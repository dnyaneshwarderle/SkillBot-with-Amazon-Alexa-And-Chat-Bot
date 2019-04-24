import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TestgroundComponent } from './testground.component';

describe('TestgroundComponent', () => {
  let component: TestgroundComponent;
  let fixture: ComponentFixture<TestgroundComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TestgroundComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TestgroundComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
