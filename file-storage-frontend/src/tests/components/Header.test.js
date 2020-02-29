import React from 'react';
import { shallow } from 'enzyme';
import Header from '../../components/Header';

test('should render Header correctly', () => {
    const title = 'abc123';
    const subtitle = 'def456';
    const wrapper = shallow(<Header title={title} subtitle={subtitle} />);
    expect(wrapper).toMatchSnapshot();
});