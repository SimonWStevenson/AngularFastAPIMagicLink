import { Component } from '@angular/core';
import { Note } from './note';
import { ListService } from './list.service'

@Component({
  selector: 'app-list',
  templateUrl: './list.component.html',
  styleUrls: ['./list.component.css']
})

export class ListComponent {
  notes: Note[] = [];
  newNoteContent: string = ""

  constructor(
    private listService: ListService,
    ){}

  ngOnInit(): void {
    this.listService.getNotes().subscribe((response) => {
      this.notes = response
    });
  }

  addNote(note: string){
    note = note.trim().replace(/\n/g, '<br/>');
    if(!note){alert("Please enter a note"); return;}
    else {
      this.listService.addNote(note).subscribe((response) => {
        if (!this.notes){this.notes = [response]}
        else {this.notes.push(response)}
      })
    }
  }
}
