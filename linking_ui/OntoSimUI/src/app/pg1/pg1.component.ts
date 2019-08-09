import { Component, OnInit } from '@angular/core';
import { Appconst } from  '../util/appconst';

import { UploadService } from  '../util/upload.service';
import { ApputilService } from  '../util/apputil.service';


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

  onFileSelectedSrc1(event){
    var file:File = event.target.files[0];

    var reader:FileReader = new FileReader();
    reader.onloadend = (e) => {
      let fl_ext = file.name.split('.').pop().toLowerCase();
      if(fl_ext == Appconst.FILE_EXT){

        this.ontosim_data["msg"]["msg_val"] = ""
        this.ontosim_data["msg"]["msg_cause"] = ""

        this.ontosim_data["src_in_data"]["file_nm"] = file.name;
        this.ontosim_data["src_in_data"]["file_typ"] = file.type;
        this.ontosim_data["src_in_data"]["file"] = reader.result;

      }else{

          this.ontosim_data["msg"]["msg_val"] = Appconst.ERR_MSG
          this.ontosim_data["msg"]["msg_cause"] = Appconst.ERR_MSG_1

      }

    }

    reader.readAsDataURL(file); //Base64
  }

  onFileSelectedTrgt1(event){
    var file:File = event.target.files[0];

    var reader:FileReader = new FileReader();
    reader.onloadend = (e) => {


      let fl_ext = file.name.split('.').pop().toLowerCase();
      if(fl_ext == Appconst.FILE_EXT){


        this.ontosim_data["msg"]["msg_val"] = ""
        this.ontosim_data["msg"]["msg_cause"] = ""

        this.ontosim_data["trgt_in_data"]["file_nm"] = file.name;
        this.ontosim_data["trgt_in_data"]["file_typ"] = file.type;
        this.ontosim_data["trgt_in_data"]["file"] = reader.result;

      }else{

          this.ontosim_data["msg"]["msg_val"] = Appconst.ERR_MSG
          this.ontosim_data["msg"]["msg_cause"] = Appconst.ERR_MSG_1

      }

    }

    reader.readAsDataURL(file); //Base64
  }


  callJavaWS(){

    this.ontosim_data["msg"]["msg_val"] = ""
    this.ontosim_data["msg"]["msg_cause"] = ""

   this._uploadService.call_onto_service(this.ontosim_data, 'java')
   .subscribe(result => {

	    if(result["msg"] && result["msg"]["msg_val"] != ''){
	          this.ontosim_data["msg"]["msg_val"] = result["msg"]["msg_val"]
	          this.ontosim_data["msg"]["msg_cause"] = result["msg"]["msg_cause"]
	    }else{
	          this._uploadService.call_onto_service(result, 'py')
	          .subscribe(result2 => {
	            	this._apputilService.downloadFile(result2["final_op_data"]);
	          },
	          (error2) => {
	          	this.ontosim_data["msg"]["msg_val"] = Appconst.ERR_MSG
	          	this.ontosim_data["msg"]["msg_cause"] = error2.message
	          }
   		  );
  	    }
    },
    (error) => {

          this.ontosim_data["msg"]["msg_val"] = Appconst.ERR_MSG
          this.ontosim_data["msg"]["msg_cause"] = error.message

    }
    );

  }





}
