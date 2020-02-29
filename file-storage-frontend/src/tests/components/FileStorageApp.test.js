import React from 'react';
import { shallow } from 'enzyme';
import FileStorageApp from '../../components/FileStorageApp';

test('should render FileStorageApp correctly', () => {
    const fetch = jest.fn(() => Promise.resolve());
    const wrapper = shallow(<FileStorageApp fetch={fetch} />);
    expect(fetch).toHaveBeenCalled();
    expect(wrapper).toMatchSnapshot();
});