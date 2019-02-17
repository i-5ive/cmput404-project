import Reflux from "reflux";

import Actions from "./FriendsActions";

import RestUtil from "../util/RestUtil";

const makeUserQueryObject = (user) => {
    return {
        id: user.id,
        host: user.host,
        displayName: user.displayName,
        url: user.url
    };
};

/**
 * This store keeps track of the state of components that deal with user friend requests
 */
export default class FriendsStore extends Reflux.Store {
    constructor() {
        super();
        this.state = {
            errorLoadingRequests: false,
            friendRequests: [],
            loadingRequests: false,
            sendingFriendRequest: false,
            successfullySentRequest: false,
            failedToSendRequest: false
        };
        this.listenables = Actions;

        if (process.env.NODE_ENV === "development") {
            window.DEV_FRIENDS_STORE = this;
        }
    }

    onLoadFriendRequests(user) {
        this.setState({
            loadingRequests: true,
            errorLoadingRequests: false
        });

        RestUtil.sendGET(`author/${user.id}/friendrequests/`).then((requests) => {
            this.setState({
                friendRequests: requests,
                loadingRequests: false
            });
        }).catch((err) => {
            this.setState({
                loadingRequests: false,
                errorLoadingRequests: true
            });
            console.error(err);
        });
    }

    onSendFriendRequest(user, friend) {
        this.setState({
            sendingFriendRequest: true,
            successfullySentRequest: false,
            failedToSendRequest: false
        });

        RestUtil.sendPOST("friendrequest/", {
            query: "friendrequest",
            author: makeUserQueryObject(user),
            friend: makeUserQueryObject(friend)
        }).then(() => {
            this.setState({
                sendingFriendRequest: false,
                successfullySentRequest: true,
                failedToSendRequest: false
            });
        }).catch((err) => {
            this.setState({
                sendingFriendRequest: false,
                successfullySentRequest: false,
                failedToSendRequest: true
            });
            console.error(err);
        });
    }
}
