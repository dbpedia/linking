import { Component, OnInit, ElementRef } from '@angular/core';
import { Appconst } from  '../util/appconst';

import { UploadService } from  '../util/upload.service';
import { ApputilService } from  '../util/apputil.service';


@Component({
  selector: 'app-pg1',
  templateUrl: './pg1.component.html',
  providers: [ UploadService, ApputilService, Appconst  ],
  styleUrls: ['pg1_component.css']
})


export class Pg1Component implements OnInit {

  ontosim_data = null;
  el = null;

  constructor(
  private _uploadService: UploadService,
  private _apputilService: ApputilService,
  public _element: ElementRef) { }

  ngOnInit() {
    this.ontosim_data = this._apputilService.getJSON();
    this.el = this._element.nativeElement;
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

          this.makeActivate()
          
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

          this.makeActivate()

          this.ontosim_data["msg"]["msg_val"] = Appconst.ERR_MSG
          this.ontosim_data["msg"]["msg_cause"] = Appconst.ERR_MSG_1

      }

    }

    reader.readAsDataURL(file); //Base64
  }


  callJavaWS(){

    this.ontosim_data["msg"]["msg_val"] = ""
    this.ontosim_data["msg"]["msg_cause"] = ""
    this.makeDeactivate()
    
   this._uploadService.call_onto_service(this.ontosim_data, 'java')
   .subscribe(result => {

      console.log('1')
	    if(result["msg"] && result["msg"]["msg_val"] != ''){

            console.log('1')
            this.makeActivate()
            console.log('2')

	          this.ontosim_data["msg"]["msg_val"] = result["msg"]["msg_val"]
	          this.ontosim_data["msg"]["msg_cause"] = result["msg"]["msg_cause"]

	    }else{

	          this._uploadService.call_onto_service(result, 'py')
	          .subscribe(result2 => {
                
                this.makeActivate()

	            	this._apputilService.downloadFile(result2["final_op_data"]);
	          },
	          (error2) => {

              console.log('1')
              this.makeActivate()
              console.log('3')

	          	this.ontosim_data["msg"]["msg_val"] = Appconst.ERR_MSG
	          	this.ontosim_data["msg"]["msg_cause"] = error2.message
	          }
   		  );
  	    }
    },
    (error) => {

          console.log('1')
          this.makeActivate()
          console.log('3')

          this.ontosim_data["msg"]["msg_val"] = Appconst.ERR_MSG
          this.ontosim_data["msg"]["msg_cause"] = error.message

    }
    );

  }


  makeDeactivate(){

    this.el.querySelector('#ontoBtnDiv').disabled = true
    this.el.querySelector('#loadingIndicator').style.display = "block";



  }

  makeActivate(){

    console.log('2')
    this.el.querySelector('#ontoBtnDiv').disabled = false
    this.el.querySelector('#loadingIndicator').style.display = "none";
  
  }


}
