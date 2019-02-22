import Reflux from "reflux";

import update from "immutability-helper";

import Actions from "./ProfileActions";
import RestUtil from "../util/RestUtil";
import { POSTS_PAGE_SIZE } from "../constants/PostConstants";

/**
 * This store keeps track of the state of components that deal with a user profile
 */
export default class ProfileStore extends Reflux.Store {
    constructor() {
        super();
        this.state = {
            isLoadingProfile: false,
            posts: []
        };
        this.listenables = Actions;

        if (process.env.NODE_ENV === "development") {
            window.DEV_PROFILE_STORE = this;
        }
    }

    /**
     * Loads data about a user's profile
     * @param {String} id - the ID of the user to load data for
     */
    onLoadProfileDetails(id) {
        this.setState({
            isLoadingProfile: true,
            successfullyLoadedProfile: false,
            errorLoadingProfile: false,
            github: null,
            posts: [],
            isFriendsWithUser: null,
            sentFriendRequestToUser: null,
            profileActionSuccess: null,
            profileActionError: null,
            isFollowingUser: null,
            isProfileActionDisabled: false
        });

        RestUtil.sendGET(`author/${id}/`).then((res) => {
            this.setState({
                isLoadingProfile: false,
                successfullyLoadedProfile: true,
                profileDetails: res.data,
                canSaveProfile: true
            });
        }).catch((err) => {
            this.setState({
                isLoadingProfile: false,
                errorLoadingProfile: true
            });
            console.error(err);
        });
    }

    /**
     * Loads the specified user's activity stream
     * @param {String} id - the ID of the user
     * @param {number} page - the page number to load data from
     */
    onLoadActivityStream(id, page) {
        this.setState({
            isLoadingStream: true,
            errorLoadingStream: false
        });
        RestUtil.sendGET(`author/${id}/posts/`, {
            page: page,
            size: POSTS_PAGE_SIZE
        }).then((res) => {
            const posts = update(this.state.posts, {
                $push: res.data.posts
            });
            this.setState({
                isLoadingStream: false,
                hasNextActivityPage: Boolean(res.data.next),
                posts: posts
            });
        }).catch((err) => {
            this.setState({
                isLoadingStream: false,
                errorLoadingStream: true
            });
            console.error(err);
        });
    }

    /**
     * Handles a user updating their profile information
     * @param {String} id - the id of the user
     * @param {Object} data - the user's new profile data
     */
    onSaveProfileDetails(id, data) {
        this.setState({
            isSavingProfile: true,
            successfullySavedProfile: false,
            errorSavingProfile: false
        });

        RestUtil.sendPOST(`author/${id}/update/`, data).then(() => {
            const newProfile = update(this.state.profileDetails, {
                $merge: data
            });
            this.setState({
                isSavingProfile: false,
                successfullySavedProfile: true,
                profileDetails: newProfile
            });
        }).catch((err) => {
            this.setState({
                isSavingProfile: false,
                errorSavingProfile: true
            });
            console.error(err);
        });
    }

    /**
     * Handles the user opening the modal that allows editing profile details
     */
    onInitEditProfileDetails() {
        const initialState = {
            firstName: "",
            lastName: "",
            github: "",
            email: "",
            bio: ""
        };
        this.setState({
            editProfileDetails: Object.assign(initialState, this.state.profileDetails),
            editProfileValidity: {}
        });
    }

    onSetDisplayName(value) {
        const details = update(this.state.editProfileDetails, {
            $merge: {
                displayName: value
            }
        });
        this.setState({
            editProfileDetails: details
        });
    }

    onSetFirstName(value) {
        const details = update(this.state.editProfileDetails, {
            $merge: {
                firstName: value
            }
        });
        this.setState({
            editProfileDetails: details
        });
    }

    onSetLastName(value) {
        const details = update(this.state.editProfileDetails, {
            $merge: {
                lastName: value
            }
        });
        this.setState({
            editProfileDetails: details
        });
    }

    onSetEmailAddress(value) {
        const details = update(this.state.editProfileDetails, {
            $merge: {
                email: value
            }
        });
        this.setState({
            editProfileDetails: details
        });
    }

    onSetGithubLink(value) {
        const details = update(this.state.editProfileDetails, {
            $merge: {
                github: value
            }
        });
        this.setState({
            editProfileDetails: details
        });
    }

    onSetBio(value) {
        const details = update(this.state.editProfileDetails, {
            $merge: {
                bio: value
            }
        });
        this.setState({
            editProfileDetails: details
        });
    }

    /**
     * Loads the friend status between two users
     * @param {String} profileId - the ID of the profile being viewed
     * @param {String} viewerId - the ID of the user viewing the profile (must be a local user)
     */
    // TODO: implement the 2 below endpoints
    onLoadFriendStatus(profileId, viewerId) {
        this.setState({
            isLoadingFriendStatus: true,
            errorLoadingFriendStatus: false
        });
        RestUtil.sendPOST(`author/${viewerId}/friendStatus/`, {
            author: profileId
        }).then((res) => {
            this.setState({
                isLoadingFriendStatus: false,
                isFriendsWithUser: res.data.isFriendsWithUser,
                isFollowingUser: res.data.isFollowingUser
            });
        }).catch((err) => {
            this.setState({
                isLoadingFriendStatus: false,
                errorLoadingFriendStatus: true
            });
            console.error(err);
        });
    }

    onUnfriendUser(author, requester) {
        this.setState({
            isProfileActionDisabled: true,
            profileActionError: null,
            profileActionSuccess: null
        });
        RestUtil.sendPOST("unfriend/", {
            author: author,
            requester: requester
        }).then(() => {
            this.setState({
                isProfileActionDisabled: false,
                profileActionSuccess: "This user is no longer friends with you",
                isFriendsWithUser: false,
                isFollowingUser: false
            });
        }).catch((err) => {
            this.setState({
                isProfileActionDisabled: false,
                profileActionError: "An error occurred while unfriending this user"
            });
            console.error(err);
        });
    }

    onSendFriendRequest(friend, requester) {
        this.setState({
            isProfileActionDisabled: true,
            profileActionError: null,
            profileActionSuccess: null
        });
        RestUtil.sendPOST("friendrequest/", {
            author: requester,
            friend: friend,
            query: "friendrequest"
        }).then(() => {
            this.setState({
                isProfileActionDisabled: false,
                profileActionSuccess: "Your friend request has been sent.",
                sentFriendRequestToUser: false,
                isFollowingUser: true
            });
        }).catch((err) => {
            this.setState({
                isProfileActionDisabled: false,
                profileActionError: "An error occurred while sending your friend request."
            });
            console.error(err);
        });
    }
}
