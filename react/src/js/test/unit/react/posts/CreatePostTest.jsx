import React from "react";
import { expect } from "chai";
import { shallow } from "enzyme";

import CreatePost from "react/posts/CreatePost";

describe("CreatePost Tests", () => {
    it("should render", () => {
        const wrapper = shallow(<CreatePost />);
        expect(wrapper.find(".create-post-wrapper")).to.have.lengthOf(1);
    });
});
