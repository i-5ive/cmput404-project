import React from "react";
import { expect } from "chai";
import Post from "react/posts/Post";
import { shallow } from "enzyme";

describe("Post Tests", () => {
    it("renders via shallow", () => {
        const page = shallow(<Post />);

        expect(page.contains(<p/>));
    });
});
