import React from "react";
import { expect } from "chai";
import { shallow } from "enzyme";
import sinon from "sinon";

import FriendRequestView from "react/friends/FriendRequestView";
import FriendsActions from "react/friends/FriendsActions";

const MOCK_USER_INFO = {
    id: "abc-defg-hijkl"
};

const request1 = {
    id: "http://127.0.0.1/author/1",
    displayName: "Request 1",
    host: "http://127.0.0.1",
    url: "http://127.0.0.1/author/1"
};

describe("Friend requests list view tests", () => {
    let sandbox = null;

    beforeEach(() => {
        sandbox = sinon.createSandbox();
    });

    it("should allow clicking buttons when actions are not disabled", () => {
        const wrapper = shallow(<FriendRequestView request={request1} disableActions={false} />);
        wrapper.instance().store.singleton.setState({
			userInfo: MOCK_USER_INFO
        });
        expect(wrapper.find("Button").at(0).props().disabled).eql(false);
        expect(wrapper.find("Button").at(1).props().disabled).eql(false);
    });

    it("should not allow clicking buttons when actions are disabled", () => {
        const wrapper = shallow(<FriendRequestView request={request1} disableActions />);
        wrapper.instance().store.singleton.setState({
			userInfo: MOCK_USER_INFO
        });
        expect(wrapper.find("Button").at(0).props().disabled).eql(true);
        expect(wrapper.find("Button").at(1).props().disabled).eql(true);
    });

    it("tests the display name showing up", () => {
        const wrapper = shallow(<FriendRequestView request={request1} />);
        wrapper.instance().store.singleton.setState({
			userInfo: MOCK_USER_INFO
        });
        expect(wrapper.find("Link.name").text()).eql(request1.displayName);
    });

    it("tests that the approve action is invoked after clicking approve", () => {
        const action = sandbox.spy(FriendsActions, "respondToFriendRequest");
        const wrapper = shallow(<FriendRequestView request={request1} />);
        wrapper.instance().store.singleton.setState({
			userInfo: MOCK_USER_INFO
        });
        wrapper.find("Button").at(0).simulate("click");
        expect(action.calledOnce).to.be.true;
        expect(action.calledWith(MOCK_USER_INFO.id, request1, true));
    });

    it("tests that the reject action is invoked after clicking reject", () => {
        const action = sandbox.spy(FriendsActions, "respondToFriendRequest");
        const wrapper = shallow(<FriendRequestView request={request1} />);
        wrapper.instance().store.singleton.setState({
			userInfo: MOCK_USER_INFO
        });
        wrapper.find("Button").at(1).simulate("click");
        expect(action.calledOnce).to.be.true;
        expect(action.calledWith(MOCK_USER_INFO.id, request1, false));
    });

    afterEach(() => {
        sandbox.restore();
    });
});
