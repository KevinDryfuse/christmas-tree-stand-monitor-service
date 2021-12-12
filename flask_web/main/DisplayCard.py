from flask_web.enums.Status import Status


class DisplayCard:

    def get_color(self, status):
        color = "secondary"

        if status == Status.linked.value:
            color = "primary"
        elif status == Status.reset.value:
            color = "info"
        elif status == Status.full.value:
            color = "primary"
        elif status == Status.acceptable.value:
            color = "success"
        elif status == Status.low.value:
            color = "danger"

        return color

    def get_icon(self, status):

        icon = "fas fa-question fa-2x"

        if status == Status.linked.value:
            icon = "fas fa-link fa-2x"
        elif status == Status.reset.value:
            icon = "fas fa-play fa-2x"
        elif status == Status.full.value:
            icon = "fas fa-battery-full fa-2x"
        elif status == Status.acceptable.value:
            icon = "fas fa-battery-half fa-2x"
        elif status == Status.low.value:
            icon = "fas fa-battery-empty fa-2x"

        return icon

