import {expect} from "chai";
import sinon from "sinon";

import FriendsStore from "react/friends/FriendsStore";
import RestUtil from "react/util/RestUtil";

import {createMockPromise} from "../../util/PromiseUtil";

const MOCK_USER_INFO = {
    id: "abc-defg-hijkl"
};

const MOCK_REQUEST = {
    id: "http://127.0.0.1/author/1",
    displayName: "Request 1",
    host: "http://127.0.0.1",
    url: "http://127.0.0.1/author/1"
};

const FRIEND_REQUESTS = [];
for (let i = 0; i < 25; ++i) {
    FRIEND_REQUESTS.push({
        id: `http://127.0.0.1/author/${i}`,
        displayName: `Request ${i}`,
        host: "http://127.0.0.1",
        url: `http://127.0.0.1/author/${i}`
    });
}

describe("Friend store tests", () => {
    let sandbox = null;
    let store = null;

    beforeEach(() => {
        sandbox = sinon.createSandbox();
        store = new FriendsStore();
    });

    it("Tests fetching friend requests successfully", () => {
        const getStub = sandbox.stub(RestUtil, "sendGET").returns(createMockPromise({data: FRIEND_REQUESTS}));
        store.onLoadFriendRequests(MOCK_USER_INFO);
        expect(getStub.calledOnce).to.be.true;
        expect(store.state.friendRequests).to.be.eql(FRIEND_REQUESTS);
    });

    describe("Responding to friend requests", () => {
        it("Tests responding to a friend request when there is only one", () => {
            store.setState({
                friendRequests: [MOCK_REQUEST]
            });
            const postStub = sandbox.stub(RestUtil, "sendPOST").returns(createMockPromise());
            store.onRespondToFriendRequest(MOCK_USER_INFO.id, MOCK_REQUEST, true);
            expect(postStub.calledOnce).to.be.true;
            expect(store.state.friendRequests.length).to.be.eql(0);
        });

        it("Tests responding to the fifth friend request when there are multiple", () => {
            store.setState({
                friendRequests: FRIEND_REQUESTS
            });
            const postStub = sandbox.stub(RestUtil, "sendPOST").returns(createMockPromise());
            store.onRespondToFriendRequest(MOCK_USER_INFO.id, FRIEND_REQUESTS[4], true);
            expect(postStub.calledOnce).to.be.true;
            const expectedRequests = FRIEND_REQUESTS.filter((req, i) => i != 4);
            expect(store.state.friendRequests).to.be.eql(expectedRequests);
        });

        it("Tests responding to the first friend request when there are multiple", () => {
            store.setState({
                friendRequests: FRIEND_REQUESTS
            });
            const postStub = sandbox.stub(RestUtil, "sendPOST").returns(createMockPromise());
            store.onRespondToFriendRequest(MOCK_USER_INFO.id, FRIEND_REQUESTS[0], true);
            expect(postStub.calledOnce).to.be.true;
            const expectedRequests = FRIEND_REQUESTS.filter((req, i) => i != 0);
            expect(store.state.friendRequests).to.be.eql(expectedRequests);
        });

        it("Tests responding to the last friend request when there are multiple", () => {
            store.setState({
                friendRequests: FRIEND_REQUESTS
            });
            const postStub = sandbox.stub(RestUtil, "sendPOST").returns(createMockPromise());
            store.onRespondToFriendRequest(MOCK_USER_INFO.id, FRIEND_REQUESTS[FRIEND_REQUESTS.length - 1], true);
            expect(postStub.calledOnce).to.be.true;
            const expectedRequests = FRIEND_REQUESTS.filter((req, i) => i != FRIEND_REQUESTS.length - 1);
            expect(store.state.friendRequests).to.be.eql(expectedRequests);
        });
    });

    afterEach(() => {
        sandbox.restore();
    });
});