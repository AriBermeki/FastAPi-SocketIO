class DynamicChart:
    def __init__(
        self, 
        chart_type, 
        real_time, 
        container_id, 
        data, 
        tooltip, 
        x_field, 
        y_field, 
        title_visible, 
        title_text, 
        description_text, 
        description_visible, 
        force_fit, 
        padding, 
        smooth, 
        width, 
        height, 
        theme, 
        series_field, 
        legend_position, 
        responsive, 
        animation, 
        x_axis, 
        y_axis, 
        legend_visible, 
        angle_field, 
        color_field, 
        meta, 
        bin_number, 
        color, 
        point_visible, 
        min_value, 
        max_value, 
        tooltip_visible, 
        legend_flip_page
        ):
        self.chart_type = chart_type
        self.real_time = real_time
        self.container_id = container_id
        self.data = data
        self.tooltip = tooltip
        self.x_field = x_field
        self.y_field = y_field
        self.title_visible = title_visible
        self.title_text = title_text
        self.description_text = description_text
        self.description_visible = description_visible
        self.force_fit = force_fit
        self.padding = padding
        self.smooth = smooth
        self.width = width
        self.height = height
        self.theme = theme
        self.series_field = series_field
        self.legend_position = legend_position
        self.responsive = responsive
        self.animation = animation
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.legend_visible = legend_visible
        self.angle_field = angle_field
        self.color_field = color_field
        self.meta = meta
        self.bin_number = bin_number
        self.color = color
        self.point_visible = point_visible
        self.min_value = min_value
        self.max_value = max_value
        self.tooltip_visible = tooltip_visible
        self.legend_flip_page = legend_flip_page

    def to_dict(self):
        return {
            'chart_type': self.chart_type,
            'real_time': self.real_time,
            'container_id': self.container_id,
            'data': self.data,
            'tooltip': self.tooltip,
            'xField': self.x_field,
            'yField': self.y_field,
            'title_visible': self.title_visible,
            'title_text': self.title_text,
            'description_text': self.description_text,
            'description_visible': self.description_visible,
            'force_fit': self.force_fit,
            'padding': self.padding,
            'smooth': self.smooth,
            'width': self.width,
            'height': self.height,
            'theme': self.theme,
            'series_field': self.series_field,
            'legend_position': self.legend_position,
            'responsive': self.responsive,
            'animation': self.animation,
            'xAxis': self.x_axis,
            'yAxis': self.y_axis,
            'legend_visible': self.legend_visible,
            'angle_field': self.angle_field,
            'color_field': self.color_field,
            'meta': self.meta,
            'bin_number': self.bin_number,
            'color': self.color,
            'point_visible': self.point_visible,
            'min_value': self.min_value,
            'max_value': self.max_value,
            'tooltip_visible': self.tooltip_visible,
            'legend_flip_page': self.legend_flip_page
        }