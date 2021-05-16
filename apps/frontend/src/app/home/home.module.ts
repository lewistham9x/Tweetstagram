import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HomeRoutingModule } from './home-routing.module';
import { CoreModule } from '../core/core.module';
import { SlideshowModule } from 'ng-simple-slideshow';
// import { LazyLoadImageModule } from 'ng-lazyload-image';

import { HomepageComponent } from './homepage/homepage.component';
import { FeedCardComponent } from './homepage/feed-card/feed-card.component';
import { FeedCommentsComponent } from './homepage/feed-card/feed-comments/feed-comments.component';
import { FeedImagesComponent } from './homepage/feed-card/feed-images/feed-images.component';

@NgModule({
	declarations: [
		HomepageComponent,
		FeedCardComponent,
		FeedCommentsComponent,
		FeedImagesComponent
	],
	imports: [CommonModule, CoreModule, HomeRoutingModule, SlideshowModule]
})
export class HomeModule {}
