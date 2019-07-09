import { TestBed } from '@angular/core/testing';

import { ApputilService } from './apputil.service';

describe('ApputilService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: ApputilService = TestBed.get(ApputilService);
    expect(service).toBeTruthy();
  });
});
