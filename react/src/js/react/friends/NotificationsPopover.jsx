import React from "react";
import Reflux from "reflux";

import FriendsStore from "./FriendsStore";

export default class NotificationsPopover extends Reflux.Component {
    constructor() {
        super();
        this.store = FriendsStore;
    }

    render() {
        return (
            <div>
                WOWWWWW A DROPDOWN!
            </div>
        );
    }
}
