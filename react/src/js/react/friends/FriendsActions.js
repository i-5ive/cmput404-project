import Reflux from "reflux";

const Actions = Reflux.createActions([
    "loadFriendRequests",
    "sendFriendRequest",
    "respondToFriendRequest",
    "removeFriendRequest"
]);

export default Actions;
