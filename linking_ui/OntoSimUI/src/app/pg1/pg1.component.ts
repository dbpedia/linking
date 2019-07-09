import { Component, OnInit } from '@angular/core';
import { Appconst } from  '../util/appconst';

import { UploadService } from  '../util/upload.service';
import { ApputilService } from  '../util/apputil.service';

import { Pg3Component } from '../pg3/pg3.component';


@Component({
  selector: 'app-pg1',
  templateUrl: './pg1.component.html',
  providers: [ UploadService, ApputilService, Appconst  ],
  styles: []
})


export class Pg1Component implements OnInit {

  ontosim_data = null;
  constructor(private _uploadService: UploadService,private _apputilService: ApputilService) { }

  ngOnInit() {
    this.ontosim_data = this._apputilService.getJSON();
  }

  onFileSelectedSrc(event){
    var file:File = event.target.files[0];

    var reader:FileReader = new FileReader();
    reader.onloadend = (e) => {
      this.ontosim_data["src_in_data"]["file_nm"] = file.name;
      this.ontosim_data["src_in_data"]["file_typ"] = file.type;
      this.ontosim_data["src_in_data"]["file"] = reader.result;
    }

    reader.readAsDataURL(file); //Base64

  }

  onFileSelectedTrgt(event){
    var file:File = event.target.files[0];

    var reader:FileReader = new FileReader();
    reader.onloadend = (e) => {
      this.ontosim_data["trgt_in_data"]["file_nm"] = file.name;
      this.ontosim_data["trgt_in_data"]["file_typ"] = file.type;
      this.ontosim_data["trgt_in_data"]["file"] = reader.result;
    }

    reader.readAsDataURL(file); //Base64

  }


  uploadOWLFile(){
    this.ontosim_data["ind"]["service_ind"] = Appconst.javaInd;
    this.ontosim_data["ind"]["op_ind"] = Appconst.javaInd_1;

    this._uploadService.call_onto_service(this.ontosim_data)
    .subscribe(result => {

    	this._apputilService.downloadFile(result["src_op_data"]);
    	this._apputilService.downloadFile(result["trgt_op_data"]);

    } );

    //let saro = new Pg3Component();
    //let retVal = saro.func("hi");
    //console.log(retVal);

  }


}
