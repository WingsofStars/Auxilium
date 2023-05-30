import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
// import * as fsPromise from 'fs/promises'; 
// const locationFile = await fsPromise.open('/home/auxilium/important_text_files/zipcode.txt', 'r');
// const ownerNameFile = await fsPromise.open('/home/auxilium/important_text_files/ownername.txt', 'r');
// const assistantNameFile = await fsPromise.open('/home/auxilium/important_text_files/assistant_name.txt', 'r');

@Component({
  selector: 'app-landing-page',
  templateUrl: './landing-page.component.html',
  styleUrls: ['./landing-page.component.css']
})
export class LandingPageComponent {
  
  // locations;
  // owners;
  // assistants;
  constructor(private http: HttpClient){
    this.loadAssistantName()
    this.loadOwnerName()
    this.loadLocation()
    // this.locations = locationFile.readLines();
    // this.owners = ownerNameFile.readLines();
    // this.assistants = assistantNameFile.readLines();
    // console.log(this.locations)
    console.log(this.location)
  }
  loadAssistantName() {
    this.http.get('../assets/assistant_name.txt', { responseType: 'text' })
      .subscribe(data => this.assistantName = data);
  }
  loadOwnerName() {
    this.http.get('assets/ownername.txt', { responseType: 'text' })
      .subscribe(data => this.ownerName = data);
  }
  loadLocation() {
    this.http.get('../assets/zipcode.txt', { responseType: 'text' })
      .subscribe(data => this.location = data);
  }
  

  assistantName: string = "";
  ownerName: string = "";
  location: string = "";


}


