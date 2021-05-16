import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AuthGuardService } from './core/guards/auth-guard.service';
import { LoginComponent } from './auth/login/login.component';
import { RegisterComponent } from './auth/register/register.component';
import { ForgotPasswordComponent } from './auth/forgot-password/forgot-password.component';
import { HomepageComponent } from './home/homepage/homepage.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';

const routes: Routes = [
	{ path: '', component: HomepageComponent, pathMatch: 'full' },
	{ path: '404', component: PageNotFoundComponent },
	{
		path: 'notifications',
		loadChildren: () =>
			import('../app/notification/notification.module').then(
				m => m.NotificationModule
			)
	},
	{
		path: 'explore',
		loadChildren: () =>
			import('../app/explore/explore.module').then(m => m.ExploreModule)
	},
	{
		path: 'settings',
		loadChildren: () =>
			import('../app/settings/settings.module').then(
				m => m.SettingsModule
			)
	},
	{
		path: '**',
		loadChildren: () =>
			import('../app/profile/profile.module').then(m => m.ProfileModule)
	}
];

@NgModule({
	imports: [RouterModule.forRoot(routes, { useHash: true })],
	exports: [RouterModule]
})
export class AppRoutingModule {}
