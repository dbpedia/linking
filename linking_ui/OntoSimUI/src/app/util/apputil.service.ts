import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import ontosimJSONData from '../../assets/ontosim.json';
import { Appconst } from  '../util/appconst';

@Injectable({
  providedIn: 'root'
})
export class ApputilService {

  serviceUrl = "";
  constructor() { }

  public getJSON(){
   return ontosimJSONData;
 }

  public getURL(ind){
  if(ind == "java"){
    this.serviceUrl = Appconst.javaUrl;
  }
  if(ind == "py"){
    this.serviceUrl = Appconst.pyUrl;
  }
  
	return this.serviceUrl;

  }


  public dataURItoBlob(dataURI) {

            // convert base64/URLEncoded data component to raw binary data held in a string
            var byteString;
            if (dataURI.split(',')[0].indexOf('base64') >= 0)
                byteString = atob(dataURI.split(',')[1]);
            else
                byteString = unescape(dataURI.split(',')[1]);

            // separate out the mime component
            var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];

            // write the bytes of the string to a typed array
            var ia = new Uint8Array(byteString.length);
            for (var i = 0; i < byteString.length; i++) {
                ia[i] = byteString.charCodeAt(i);
            }

            return new Blob([ia], {type:"application/json"});
        }

  public downloadFile(data){
    console.log(data["file_nm"]);
    console.log(data["file_typ"]);
  	var blob = this.dataURItoBlob("data:application/octet-stream;base64,"+data["file"]);
  	var file = new File([blob], data["file_nm"], {type: "application/rdf+xml"});

  	const url= window.URL.createObjectURL(file);
    

    let a = document.createElement('a');
    document.body.appendChild(a);
    a.setAttribute('style', 'display: none');
    a.href = url;
    a.download = data["file_nm"];
    a.click();
    window.URL.revokeObjectURL(url);
    a.remove();

  }



}
