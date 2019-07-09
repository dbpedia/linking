import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { HttpClientModule, HttpClient, HttpErrorResponse, HttpHeaders, HttpResponse} from '@angular/common/http';
import { Appconst } from  '../util/appconst';
import { ApputilService } from  '../util/apputil.service';

@Injectable({
  providedIn: 'root'
})

export class UploadService {

  _url = "";

  constructor(private _httpClient : HttpClient, private _apputilService: ApputilService) {}

  call_onto_service(data) {

      this._url = this._apputilService.getURL(data);

  		return this._httpClient
      .post(this._url, JSON.stringify(data), {headers: {'Content-Type': 'application/json'}});
      
  }

}
