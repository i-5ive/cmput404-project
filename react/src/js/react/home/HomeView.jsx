import React from "react";
import Reflux from "reflux";

import { Alert } from "react-bootstrap";

import PostFeed from "../posts/PostFeed";

import HomeStore from "./HomeStore";
import HomeActions from "./HomeActions";
import AuthStore from "../auth/AuthStore";

/**
 * Displays posts visible to the currently logged in user
 */
export default class HomeView extends Reflux.Component {
  constructor(props) {
    super(props);
    this.stores = [HomeStore, AuthStore];
  }

  componentDidMount() {
    if (this.state.userId) {
      HomeActions.loadPosts(1, this.state.userId);
    } else {
      this.props.history.push("/discover");
    }
  }

  componentDidUpdate(prevProps, prevState) {
    if (this.state.userId !== prevState.userId && this.state.userId) {
      HomeActions.loadPosts(1, this.state.userId);
    } else if (!this.state.userId) {
      this.props.history.push("/discover");
    }
  }

	_loadMorePosts = (pageNumber) => {
	    HomeActions.loadPosts(pageNumber, this.state.userId);
	};

	renderFilters() {
	    return (
  <div className="filter-posts-wrapper">
    <input type="checkbox" name="Friends" value="Friends" />
    <label htmlFor="Friends">Friends</label>
    <input type="checkbox" name="FOAF" value="FOAF" />
    <label htmlFor="FOAF">FOAF</label>
  </div>
	    );
	}

	render() {
	    return (
  <div className="homePage">
    {
	                this.state.errorLoadingPosts && (
	                    <Alert bsStyle="danger">
							An error ocurred while loading posts
	                    </Alert>
	                )
	            }
    {
	                this.renderFilters()
	            }
    <PostFeed posts={this.state.posts}
      isLoading={this.state.isLoadingPosts}
      loadMorePosts={HomeActions.loadPosts}
	            />
  </div>
	    );
	}
}
