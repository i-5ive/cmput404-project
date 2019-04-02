import Reflux from "reflux";

import update from "immutability-helper";

import Actions from "./ProfileActions";
import RestUtil from "../util/RestUtil";
import { POSTS_PAGE_SIZE } from "../constants/PostConstants";
import { isExternalAuthor, getAuthorId, escapeUrl } from "../util/AuthorUtil";
import FriendsActions from "../friends/FriendsActions";

/**
 * This store keeps track of the state of components that deal with a user profile
 */
export default class ProfileStore extends Reflux.Store {
    constructor() {
        super();
        this.state = {
            isLoadingProfile: false,
            posts: [],
            nextPage: null,
            followedUsers: [],
            followingUsers: []
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
            posts: [],
            sentFriendRequestToUser: null,
            profileActionSuccess: null,
            profileActionError: null,
            isFollowingUser: null,
            isProfileActionDisabled: false,
            errorLoadingFollowStatus: null,
            githubDetails: null
        });

        // Profiles from external servers need to be loaded on our back-end,
        // because some external servers require auth
        const external = isExternalAuthor(id),
            path = external ? `author/external/?authorUrl=${encodeURI(id)}` : `author/${getAuthorId(id)}/`;
        RestUtil.sendGET(path, {}).then((res) => {
            console.log(res);
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
    onLoadActivityStream(id, page = 0) {
        const state = {
                isLoadingStream: true,
                errorLoadingStream: false
            },
            external = isExternalAuthor(id),
            path = external ? `author/${escapeUrl(id)}/posts/` : `author/${getAuthorId(id)}/posts/`;
        if (page === 0) {
            state.posts = [];
        }
        this.setState(state);

        RestUtil.sendGET(path, {
            page: page,
            size: POSTS_PAGE_SIZE
        }).then((res) => {
            const posts = update(this.state.posts, {
                $push: res.data.posts
            });
            this.setState({
                isLoadingStream: false,
                nextPage: res.data.next ? (page + 1) : null,
                posts: posts
            });
        }).catch((err) => {
            this.setState({
                isLoadingStream: false,
                errorLoadingStream: true,
                nextPage: null
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

        RestUtil.sendPOST(`author/${id}/update/`, data, true).then(() => {
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
     * Loads the follow status between two users
     * @param {String} profileId - the ID of the profile being viewed
     * @param {String} viewerId - the ID of the user viewing the profile (must be a local user)
     */
    onLoadFollowStatus(profileId, viewerId) {
        this.setState({
            errorLoadingFollowStatus: false,
            isLoadingFollowStatus: true
        });
        RestUtil.sendPOST(`author/${viewerId}/follows/`, {
            author: profileId
        }).then((res) => {
            this.setState({
                isFollowingUser: res.data.isFollowingUser,
                isLoadingFollowStatus: false,
                isOtherFollowing: res.data.isOtherFollowing && res.data.isOtherFriendRequest
            });
        }).catch((err) => {
            this.setState({
                errorLoadingFollowStatus: true,
                isLoadingFollowStatus: true
            });
            console.error(err);
        });
    }

    onUnfollowUser(author, requester) {
        this.setState({
            isProfileActionDisabled: true,
            profileActionError: null,
            profileActionSuccess: null
        });
        RestUtil.sendPOST("unfollow/", {
            author: author,
            requester: requester,
            query: "unfollow"
        }).then(() => {
            const followingIndex = this.state.followingUsers.findIndex((user) => user.id === requester.id),
                followingUsers = update(this.state.followingUsers, {
                    $splice: [[followingIndex, 1]]
                }),
                friendsIndex = this.state.profileDetails.friends.findIndex((user) => user.id === requester.id),
                state = {
                    isProfileActionDisabled: false,
                    profileActionSuccess: "You are no longer following this user",
                    isFollowingUser: false,
                    followingUsers: followingUsers
                };
            if (friendsIndex > -1) {
                state.profileDetails = update(this.state.profileDetails, {
                    friends: {
                        $splice: [[friendsIndex, 1]]
                    }
                });
            }
            this.setState(state);
        }).catch((err) => {
            this.setState({
                isProfileActionDisabled: false,
                profileActionError: "An error occurred while unfollowing this user"
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
            // remove any existing friend request from the other user, because it has technically now been accepted
            FriendsActions.removeFriendRequest(friend);
            const followingUsers = update(this.state.followingUsers, {
                $push: [requester]
            });
            this.setState({
                isProfileActionDisabled: false,
                profileActionSuccess: "Your friend request has been sent.",
                sentFriendRequestToUser: false,
                isFollowingUser: true,
                followingUsers: followingUsers
            });
        }).catch((err) => {
            this.setState({
                isProfileActionDisabled: false,
                profileActionError: "An error occurred while sending your friend request."
            });
            console.error(err);
        });
    }

    /**
     * Loads details about the specified github account
     * @param {String} githubUrl - the URL to the github account to load details of
     */
    onLoadGithubDetails(githubUrl) {
        this.setState({
            errorLoadingGithubRepos: null
        });
        const account = githubUrl.split(".com/")[1];
        RestUtil.sendGET(`https://api.github.com/users/${account}/repos`, {}, true, false).then((res) => {
            this.setState({
                githubDetails: res.data.map((repo) => {
                    return {
                        name: repo.name,
                        url: repo.html_url
                    };
                })
            });
        }).catch((err) => {
            this.setState({
                errorLoadingGithubRepos: true
            });
            console.error(err);
        });
    }

    onDeletePost(id, postId) {
        this.setState({
            deletingPost: id,
            failedToDeletePost: false
        });
        RestUtil.sendDELETE(`posts/${id}/`).then(() => {
            const index = this.state.posts.findIndex((post) => post.id === id),
			 posts = update(this.state.posts, {
                    $splice: [[index, 1]]
                });
            this.setState({
                posts: posts,
                deletingPost: false,
                failedToDeletePost: false
            });
        }).catch((err) => {
            this.setState({
                deletingPost: false,
                failedToDeletePost: id
            });
            console.error(err);
        });
    }

    onEditPost(id, postId) {
        window.location.href = `post/${id}/edit`;
    }

    onLoadFollowedUsers(id) {
        this.setState({
            isLoadingFollowedUsers: true,
            failedToLoadFollowed: false,
            followedUsers: []
        });
        RestUtil.sendGET(`author/${id}/followed/`).then((res) => {
            this.setState({
                followedUsers: res.data.followed,
                isLoadingFollowedUsers: false
            });
        }).catch((err) => {
            this.setState({
                failedToLoadFollowed: true,
                isLoadingFollowedUsers: false
            });
            console.error(err);
        });
    }

    onLoadFollowingUsers(id) {
        this.setState({
            isLoadingFollowingUsers: true,
            failedToLoadFollowing: false,
            followingUsers: []
        });
        RestUtil.sendGET(`author/${id}/followers/`).then((res) => {
            this.setState({
                followingUsers: res.data.followers,
                isLoadingFollowingUsers: false
            });
        }).catch((err) => {
            this.setState({
                failedToLoadFollowing: true,
                isLoadingFollowingUsers: false
            });
            console.error(err);
        });
    }
}
