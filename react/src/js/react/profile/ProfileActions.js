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
    "loadFriendStatus",
    "unfriendUser",
    "cancelFriendRequest",
    "sendFriendRequest"
]);

export default Actions;
