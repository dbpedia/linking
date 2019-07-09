import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { Pg1Component } from './pg1/pg1.component';
import { Pg2Component } from './pg2/pg2.component';
import { Pg3Component } from './pg3/pg3.component';

const routes: Routes = [
	{path: 'pg1', component: Pg1Component},
	{path: 'pg2', component: Pg2Component},
	{path: 'pg3', component: Pg3Component}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { }
export const routingComponents = [Pg1Component, Pg2Component, Pg3Component]
