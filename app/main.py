from fastapi import FastAPI, HTTPException

from .storage import load_notes, save_notes
from .schemas import NoteCreate, NoteUpdate, NoteOut
from .utils import now_iso, new_id

app = FastAPI(title="Notes API", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/notes", response_model=list[NoteOut])
def list_notes(q: str | None = None):
    notes = load_notes()

    if q:
        q_lower = q.lower()
        notes = [
            n for n in notes
            if q_lower in n["title"].lower() or q_lower in n["content"].lower()
        ]

    notes.sort(key=lambda n: n["updated_at"], reverse=True)
    return notes


@app.get("/notes/{note_id}", response_model=NoteOut)
def get_note(note_id: str):
    for n in load_notes():
        if n["id"] == note_id:
            return n
    raise HTTPException(status_code=404, detail="Note not found")


@app.post("/notes", response_model=NoteOut, status_code=201)
def create_note(payload: NoteCreate):
    notes = load_notes()
    note = {
        "id": new_id(),
        "title": payload.title.strip(),
        "content": payload.content.strip(),
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    notes.append(note)
    save_notes(notes)
    return note


@app.put("/notes/{note_id}", response_model=NoteOut)
def update_note(note_id: str, payload: NoteUpdate):
    notes = load_notes()
    for n in notes:
        if n["id"] == note_id:
            if payload.title is not None:
                n["title"] = payload.title.strip()
            if payload.content is not None:
                n["content"] = payload.content.strip()

            n["updated_at"] = now_iso()
            save_notes(notes)
            return n

    raise HTTPException(status_code=404, detail="Note not found")


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: str):
    notes = load_notes()
    new_notes = [n for n in notes if n["id"] != note_id]

    if len(new_notes) == len(notes):
        raise HTTPException(status_code=404, detail="Note not found")

    save_notes(new_notes)
    return None