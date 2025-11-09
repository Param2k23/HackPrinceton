# calendar_api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List
import uvicorn
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ---------- Google Calendar Setup ----------
SERVICE_ACCOUNT_FILE = "service_account.json"  # path to your key
SCOPES = ["https://www.googleapis.com/auth/calendar"]

try:
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    calendar_service = build("calendar", "v3", credentials=credentials)
except Exception as e:
    print("⚠️ Could not initialize Google Calendar API:", e)
    calendar_service = None


# ---------- FastAPI Setup ----------
app = FastAPI(title="Family Calendar API (Google-powered)")


class FindFreeSlotsRequest(BaseModel):
    calendars: List[str]  # calendar IDs or emails
    start: datetime
    end: datetime
    duration_minutes: int = 60


class FreeSlot(BaseModel):
    start: datetime
    end: datetime


class FindFreeSlotsResponse(BaseModel):
    suggestions: List[FreeSlot]


class AddEventRequest(BaseModel):
    calendar_id: str
    title: str
    start: datetime
    end: datetime
    description: str = ""
    attendees: List[str] = []


# ---------- Utility Functions ----------

def make_timezone_aware(dt):
    """Convert naive datetime to UTC timezone-aware datetime"""
    if dt.tzinfo is None:
        from datetime import timezone
        return dt.replace(tzinfo=timezone.utc)
    return dt


def query_freebusy(calendars: List[str], start: datetime, end: datetime):
    # Ensure datetimes are timezone-aware
    start = make_timezone_aware(start)
    end = make_timezone_aware(end)
    
    body = {
        "timeMin": start.isoformat(),
        "timeMax": end.isoformat(),
        "items": [{"id": c} for c in calendars],
    }
    events_result = calendar_service.freebusy().query(body=body).execute()
    return events_result["calendars"]


def merge_busy_periods(busy_periods):
    """Combine overlapping busy times."""
    if not busy_periods:
        return []
    busy_periods.sort(key=lambda x: x["start"])
    merged = [busy_periods[0]]
    for current in busy_periods[1:]:
        last = merged[-1]
        if current["start"] <= last["end"]:
            last["end"] = max(last["end"], current["end"])
        else:
            merged.append(current)
    return merged


def invert_busy_to_free(busy_periods, start_window, end_window, duration_minutes):
    """Find free gaps longer than duration."""
    # Ensure all datetimes are timezone-aware
    start_window = make_timezone_aware(start_window)
    end_window = make_timezone_aware(end_window)
    
    free_slots = []
    cursor = start_window
    
    for period in busy_periods:
        period_start = make_timezone_aware(period["start"])
        period_end = make_timezone_aware(period["end"])
        
        if period_start > cursor:
            gap = (period_start - cursor).total_seconds() / 60
            if gap >= duration_minutes:
                free_slots.append({"start": cursor, "end": period_start})
        cursor = max(cursor, period_end)
    
    if (end_window - cursor).total_seconds() / 60 >= duration_minutes:
        free_slots.append({"start": cursor, "end": end_window})
    
    return free_slots


# ---------- API Endpoints ----------

@app.post("/find_free_slots", response_model=FindFreeSlotsResponse)
def find_free_slots(req: FindFreeSlotsRequest):
    if not calendar_service:
        raise HTTPException(500, "Google Calendar service not initialized")

    busy_periods = []
    calendars = query_freebusy(req.calendars, req.start, req.end)

    for cal_id, data in calendars.items():
        for b in data.get("busy", []):
            busy_periods.append({
                "start": datetime.fromisoformat(b["start"].replace("Z", "+00:00")),
                "end": datetime.fromisoformat(b["end"].replace("Z", "+00:00"))
            })

    merged_busy = merge_busy_periods(busy_periods)
    free = invert_busy_to_free(merged_busy, req.start, req.end, req.duration_minutes)
    return {"suggestions": free}


@app.post("/add_event")
def add_event(req: AddEventRequest):
    if not calendar_service:
        raise HTTPException(500, "Google Calendar service not initialized")

    event = {
        "summary": req.title,
        "description": req.description,
        "start": {"dateTime": req.start.isoformat(), "timeZone": "UTC"},
        "end": {"dateTime": req.end.isoformat(), "timeZone": "UTC"},
    }
    
    # Only add attendees if provided and not empty
    # Service accounts cannot invite attendees without Domain-Wide Delegation
    if req.attendees and len(req.attendees) > 0:
        print("⚠️ Warning: Service accounts cannot invite attendees without Domain-Wide Delegation")
        print("   Creating event without attendees instead.")
        # event["attendees"] = [{"email": a} for a in req.attendees]

    try:
        result = calendar_service.events().insert(calendarId=req.calendar_id, body=event).execute()
        return {
            "eventId": result.get("id"),
            "htmlLink": result.get("htmlLink"),
            "status": "success",
            "message": "Event created successfully"
        }
    except Exception as e:
        raise HTTPException(500, f"Failed to create event: {str(e)}")


@app.get("/sync_google")
def sync_google():
    if not calendar_service:
        raise HTTPException(500, "Google Calendar service not initialized")
    return {"status": "connected", "scopes": SCOPES}


@app.get("/test_access/{calendar_id}")
def test_access(calendar_id: str):
    """Test if we can access a specific calendar"""
    if not calendar_service:
        raise HTTPException(500, "Google Calendar service not initialized")
    
    try:
        # Try to get calendar info
        cal = calendar_service.calendars().get(calendarId=calendar_id).execute()
        
        # Try to list recent events
        now = datetime.utcnow().isoformat() + 'Z'
        events_result = calendar_service.events().list(
            calendarId=calendar_id,
            timeMin=now,
            maxResults=5,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        return {
            "status": "success",
            "calendar_name": cal.get("summary", "Unknown"),
            "calendar_id": calendar_id,
            "can_read_events": True,
            "upcoming_events_count": len(events)
        }
    except Exception as e:
        return {
            "status": "error",
            "calendar_id": calendar_id,
            "message": str(e),
            "hint": "Make sure this calendar is shared with your service account"
        }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)