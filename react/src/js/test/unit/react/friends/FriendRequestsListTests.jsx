import React from "react";
import { expect } from "chai";
import { shallow } from "enzyme";

 import NotificationsPopover from "react/friends/NotificationsPopover";

 describe("Friend requests list view tests", () => {
    it("should render when there are no friend requests", () => {
        const wrapper = shallow(<NotificationsPopover />);
        wrapper.instance().store.singleton.setState({
			friendRequests: []
		});
        expect(wrapper.find("h5")).to.have.lengthOf(1);
        expect(wrapper.find("FriendRequestView")).to.have.lengthOf(0);
    });

    it("should render when there are many friend requests", () => {
        const wrapper = shallow(<NotificationsPopover />);
        const requests = [];
        for (let i = 0; i < 25; ++i) {
            requests.push({
                id: `http://127.0.0.1/author/${i}`,
                displayName: `Request ${i}`,
                host: "http://127.0.0.1",
                url: `http://127.0.0.1/author/${i}`
            });
        }
        wrapper.instance().store.singleton.setState({
			friendRequests: requests
		});
        expect(wrapper.find("FriendRequestView")).to.have.lengthOf(25);
        expect(wrapper.find('Alert[bsStyle="danger"]')).to.have.lengthOf(0);
        expect(wrapper.find('Alert[bsStyle="success"]')).to.have.lengthOf(0);
        expect(Boolean(wrapper.find('FriendRequestView').at(0).props().disableActions)).to.be.false;
    });

    it("should render an error alert if an error happened during a response", () => {
        const wrapper = shallow(<NotificationsPopover />);
        wrapper.instance().store.singleton.setState({
			friendRequests: [{
                id: "http://127.0.0.1/author/1",
                displayName: "Request 1",
                host: "http://127.0.0.1",
                url: "http://127.0.0.1/author/1"
            }],
            errorSendingResponse: true
		});
        expect(wrapper.find('Alert[bsStyle="danger"]')).to.have.lengthOf(1);
    });

    it("should disable actions when a response is being recorded", () => {
        const wrapper = shallow(<NotificationsPopover />);
        wrapper.instance().store.singleton.setState({
			friendRequests: [{
                id: "http://127.0.0.1/author/1",
                displayName: "Request 1",
                host: "http://127.0.0.1",
                url: "http://127.0.0.1/author/1"
            }],
            isRespondingToRequest: true
		});
        expect(wrapper.find('FriendRequestView').props().disableActions).to.be.true;
    });

    it("should render a success alert if a response was successfully recorded", () => {
        const wrapper = shallow(<NotificationsPopover />);
        wrapper.instance().store.singleton.setState({
			friendRequests: [{
                id: "http://127.0.0.1/author/1",
                displayName: "Request 1",
                host: "http://127.0.0.1",
                url: "http://127.0.0.1/author/1"
            }],
            successfullyRespondedToRequest: true,
            isRespondingToRequest: false
        });
        expect(wrapper.find('Alert[bsStyle="success"]')).to.have.lengthOf(1);
    });

});