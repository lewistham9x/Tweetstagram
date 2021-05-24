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
	index = 0;
	interval = 10;
	padding = 100; // padding before load
	isLoading = false; // if its loading
	isEnd = false; // if its loading

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
			this.getPosts();
		}
	};

	getPosts() {
		const url: string = this.router.url;
		const username: string = url.split('/')[1];
		console.log(this.index);
		console.log(this.index * this.interval);
		console.log(this.index * this.interval + this.interval);
		if (!this.isLoading && !this.isEnd) {
			console.log('Loading more...');
			this.isLoading = true;
			this.httpService
				.get(
					`profile/${username}/Posts?start=${
						this.index * this.interval
					}&end=${this.index * this.interval + this.interval}`
				)
				.subscribe(
					(res: any) => {
						console.log(res);
						this.posts = this.posts.concat(res.tweets);
						this.isLoading = false;
						if (res.tweets.length === 0) {
							console.log('Ended!');
							this.isEnd = true;
						}
						this.index = this.index + 1;
					},
					err => {
						console.log(err);
						this.isLoading = false;
					}
				);
		}
	}
}
