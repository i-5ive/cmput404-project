import Reflux from "reflux";

const Actions = Reflux.createActions([
    "loadProfileDetails",
    "loadActivityStream",
    "saveProfileDetails",
    "initEditProfileDetails",
    "setDisplayName",
    "setFirstName",
    "setLastName",
    "setEmailAddress",
    "setGithubLink",
    "setBio",
    "loadFollowStatus",
    "unfollowUser",
    "sendFriendRequest",
    "loadGithubDetails"
]);

export default Actions;
