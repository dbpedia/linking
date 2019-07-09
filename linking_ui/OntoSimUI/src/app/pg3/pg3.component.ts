import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-pg3',
  templateUrl: './pg3.component.html',
  styleUrls: ['./pg3.component.css']
})
export class Pg3Component implements OnInit {

  constructor() { }

  ngOnInit() {
  }

  public func(data){
  	console.log(data);
  	return data;
  }

}
