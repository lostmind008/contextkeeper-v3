#!/usr/bin/env python3
"""Test event tracking functionality"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from project_manager import ProjectManager, DevelopmentEvent, EventType, EventSeverity

# Initialize project manager
pm = ProjectManager()

# Create a test event
event = DevelopmentEvent(
    type=EventType.ERROR,
    severity=EventSeverity.CRITICAL,
    title="CORS Configuration Error",
    description="Test event for CORS error",
    project_id="proj_736df3fd80a4",
    tags=["test", "cors"]
)

print(f"Event created: {event.to_dict()}")

# Try to add the event
result = pm.add_event(event)

if result:
    print(f"✅ Event added successfully: {result.id}")
else:
    print("❌ Failed to add event")

# Get recent events
events = pm.get_recent_events(project_id="proj_736df3fd80a4", limit=5)
print(f"\nRecent events: {len(events)}")
for e in events:
    print(f"  - {e.type.value}: {e.title}")