import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { SettingsPageComponent } from './settings-page/settings-page.component';
import { SettingsComponent } from './settings.component';

const routes: Routes = [
	{
		path: '',
		component: SettingsComponent,
		children: [
			{
				path: '**',
				component: SettingsPageComponent
			}
		]
	}
];

@NgModule({
	imports: [RouterModule.forChild(routes)],
	exports: [RouterModule]
})
export class SettingsRoutingModule {}
