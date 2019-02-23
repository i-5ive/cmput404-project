import Reflux from "reflux";
import update from "immutability-helper";

import Actions from "./FriendsActions";

import RestUtil from "../util/RestUtil";

const makeUserQueryObject = (user) => {
    return {
        id: user.url,
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

        RestUtil.sendGET(`author/${user.id}/friendrequests/`).then((res) => {
            this.setState({
                friendRequests: res.data,
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

    /**
     * Handles a user responding to a friend request
     * @param {String} userId - the ID of the user responding to the request
     * @param {Object} request - the request to respond to
     * @param {boolean} approve - whether to approve the request or not
     */
    onRespondToFriendRequest(userId, request, approve) {
        this.setState({
            isRespondingToRequest: true,
            successfullyRespondedToRequest: false,
            errorSendingResponse: false
        });

        RestUtil.sendPOST(`author/${userId}/friendrequests/respond/`, {
            query: "friendResponse",
            approve: approve,
            friend: request
        }).then(() => {
            const index = this.state.friendRequests.indexOf(request),
                requests = update(this.state.friendRequests, {
                    $splice: [[index, 1]]
                });
            this.setState({
                isRespondingToRequest: false,
                successfullyRespondedToRequest: true,
                friendRequests: requests
            });
        }).catch((err) => {
            this.setState({
                isRespondingToRequest: false,
                errorSendingResponse: true
            });
            console.error(err);
        });
    }
}
