import Reflux from "reflux";

const Actions = Reflux.createActions([
    "loadFriendRequests",
    "sendFriendRequest",
    "respondToFriendRequest"
]);

export default Actions;
