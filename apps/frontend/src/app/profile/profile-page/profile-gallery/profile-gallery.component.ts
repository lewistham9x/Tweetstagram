import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import {
	faBookmark,
	faCamera,
	faUsers
} from '@fortawesome/free-solid-svg-icons';
import { HttpService } from '../../../core/services/http/http.service';

@Component({
	selector: 'ia-profile-gallery',
	templateUrl: './profile-gallery.component.html',
	styleUrls: ['./profile-gallery.component.scss']
})
export class ProfileGalleryComponent implements OnInit {
	isSelectedTab = 'Posts';
	posts: any[] = [];
	camera = faCamera;
	users = faUsers;
	bookmark = faBookmark;

	constructor(private httpService: HttpService, private router: Router) {}

	ngOnInit() {
		this.tabToggle(this.isSelectedTab);
		window.addEventListener('scroll', this.scrollEvent, true);
	}

	ngOnDestroy() {
		window.removeEventListener('scroll', this.scrollEvent, true);
	}

	scrollEvent = (event: any): void => {
		const n = event.srcElement.scrollingElement.scrollTop;
		console.log(n);
	};

	tabToggle(tabItem) {
		const url: string = this.router.url;
		const username: string = url.split('/')[1];
		this.isSelectedTab = tabItem ? tabItem : 'Posts';
		this.httpService
			.get(`profile/${username}/${this.isSelectedTab}`)
			.subscribe(
				(res: any) => {
					console.log(res);
					this.posts = res.tweets;
				},
				err => {
					console.log(err);
				}
			);
	}
}
