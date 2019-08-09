import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { Pg1Component } from './pg1/pg1.component';

const routes: Routes = [
	{path: '', component: Pg1Component},
	{path: 'pg1', component: Pg1Component},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { }
export const routingComponents = [Pg1Component]
