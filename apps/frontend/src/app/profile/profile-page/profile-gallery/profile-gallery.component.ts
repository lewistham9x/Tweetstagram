import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import {
	faBookmark,
	faCamera,
	faUsers,
} from '@fortawesome/free-solid-svg-icons';
import { HttpService } from '../../../core/services/http/http.service';

@Component({
	selector: 'ia-profile-gallery',
	templateUrl: './profile-gallery.component.html',
	styleUrls: ['./profile-gallery.component.scss'],
})
export class ProfileGalleryComponent implements OnInit {
	isSelectedTab = 'Posts';
	posts: any[] = [];
	camera = faCamera;
	users = faUsers;
	bookmark = faBookmark;
	index = 0;
	interval = 10;
	padding = 1000; // padding before load

	constructor(private httpService: HttpService, private router: Router) {}

	ngOnInit() {
		this.getPosts();
		window.addEventListener('scroll', this.scrollEvent, true);
	}

	ngOnDestroy() {
		window.removeEventListener('scroll', this.scrollEvent, true);
	}

	scrollEvent = (event: any): void => {
		const n = event.srcElement.scrollingElement.scrollTop;
		if (
			window.innerHeight + n >=
			document.body.scrollHeight - this.padding
		) {
			console.log('Loading more...');
			this.index = this.index + 1;
			this.getPosts();
		}
	};

	getPosts() {
		const url: string = this.router.url;
		const username: string = url.split('/')[1];
		this.httpService
			.get(
				`profile/${username}/Posts?start=${this.index}&end=${
					this.index + this.interval
				}`
			)
			.subscribe(
				(res: any) => {
					console.log(res);
					this.posts = this.posts.concat(res.tweets);
				},
				(err) => {
					console.log(err);
				}
			);
	}
}
