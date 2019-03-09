import React from "react";
import Reflux from "reflux";

import { Alert } from "react-bootstrap";

import ProfileActions from "./ProfileActions";
import ProfileStore from "./ProfileStore";
import LoadingComponent from "../misc/LoadingComponent";

export default class ProfilePostsStream extends Reflux.Component {
  constructor(props) {
    super(props);
    this.store = ProfileStore;
  }

  componentDidMount() {
    ProfileActions.loadActivityStream(this.props.id);
  }

  shouldComponentUpdate(prevProps, prevState) {
    return this.state.posts.length !== prevState.posts.length || this.state.errorLoadingStream !== prevState.errorLoadingStream;
  }

  render() {
    if (this.state.errorLoadingStream) {
      return (
        <Alert bsStyle="danger">
                    An error occurred while loading the user's activity stream.
        </Alert>
      );
    } else if (this.state.isLoadingStream) {
      return <LoadingComponent />;
    }
    // TODO: posts
    return (
      <div>
        {
          this.state.posts.map((post) => <div>{post.title}</div>)
        }
      </div>
    );
  }
}
