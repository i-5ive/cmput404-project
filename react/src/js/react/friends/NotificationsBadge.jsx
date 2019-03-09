import React from "react";
import Reflux from "reflux";

import { Badge } from "react-bootstrap";

import FriendsStore from "./FriendsStore";
import FriendsActions from "../friends/FriendsActions";
import AuthStore from "../auth/AuthStore";

export default class NotificationsBadge extends Reflux.Component {
  constructor() {
    super();
    this.stores = [FriendsStore, AuthStore];
  }

  componentDidMount() {
    FriendsActions.loadFriendRequests(this.state.userId);
  }

  shouldComponentUpdate(nextProps, nextState) {
    return this.state.friendRequests.length !== nextState.friendRequests.length;
  }

  render() {
    if (this.state.friendRequests.length === 0) {
      return null;
    }
    return (
      <Badge pill="true" variant="danger">
        {
          this.state.friendRequests.length
        }
      </Badge>
    );
  }
}
