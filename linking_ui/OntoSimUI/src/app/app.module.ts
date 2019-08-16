import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule, routingComponents} from './app-routing.module';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { UploadService } from  './util/upload.service';
import { AppComponent } from './app.component';


@NgModule({
  declarations: [
    AppComponent,
	routingComponents
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [ UploadService ],
  bootstrap: [AppComponent]
})

export class AppModule { }
