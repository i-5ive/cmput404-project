import Reflux from "reflux";

const Actions = Reflux.createActions([
    "loadPosts",
    "deletePost",
    "editPost",
    "reloadPosts"
]);

export default Actions;
