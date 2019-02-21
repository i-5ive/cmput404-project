import Reflux from "reflux";

import update from "immutability-helper";

import Actions from "./ProfileActions";
import RestUtil from "../util/RestUtil";
import {POSTS_PAGE_SIZE} from "../constants/PostConstants";

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
            posts: []
        });

        RestUtil.sendGET(`author/${id}/`).then((res) => {
            // TODO: remove this
            Object.assign(res.data, {
                displayName: "Mock Username aiowejoaiwejoiawieio",
                bio: "Averylogn".repeat(50),
                github: "https://github.com/amalik2"
            })
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

        RestUtil.sendPOST(`author/${id}/updateProfile/`, data).then(() => {
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
     * Load details about a user's github activity
     * @param {String} githubLink - the url of the user's github profile
     */
    /*onLoadGithubDetails(githubLink) {
        this.setState({
            isLoadingGithub: true,
            errorLoadingGithub: false,
            github: null
        });
        const username = githubLink.split(".com/")[1];
        const githubUrl = `https://api.github.com/users/${username}/events`
        RestUtil.sendGET(githubUrl, {}, true).then((res) => {
            this.setState({
                isLoadingGithub: false,
                github: {
                    activity: res.data,
                    username: username,
                    avatar: res.data[0] && res.data[0].actor.avatar_url
                }
            });
        }).catch((err) => {
            this.setState({
                errorLoadingGithub: true,
                isLoadingGithub: false
            });
            console.error(err);
        });
    }*/

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
}