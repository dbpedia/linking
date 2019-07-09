import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Pg2Component } from './pg2.component';

describe('Pg2Component', () => {
  let component: Pg2Component;
  let fixture: ComponentFixture<Pg2Component>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Pg2Component ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Pg2Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
