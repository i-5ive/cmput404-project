import React from "react";
import { expect } from "chai";
import PostPage from "react/posts/PostPage";
import PostFeed from "react/posts/PostFeed";
import { shallow } from "enzyme";

describe("PostPage Tests", () => {
    it("renders via shallow", () => {
        const page = shallow(<PostPage />);

        expect(page.contains(<PostFeed/>));
    });
});
