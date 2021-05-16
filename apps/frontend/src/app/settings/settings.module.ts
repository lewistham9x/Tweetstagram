import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { SettingsPageComponent } from './settings-page/settings-page.component';
import { SettingsRoutingModule } from './settings-routing.module';
import { SettingsComponent } from './settings.component';

library.add(fas);

@NgModule({
	declarations: [SettingsComponent, SettingsPageComponent],
	imports: [CommonModule, SettingsRoutingModule, FontAwesomeModule]
})
export class SettingsModule {}
