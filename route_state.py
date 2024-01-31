import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.qos import QoSReliabilityPolicy
from rclpy.qos import QoSDurabilityPolicy

from autoware_planning_msgs.msg import RouteState

class RouteStateViewer(Node):

    def __init__(self):
        super().__init__("route_state")
        qos = QoSProfile(depth=1, reliability=QoSReliabilityPolicy.RELIABLE, durability=QoSDurabilityPolicy.TRANSIENT_LOCAL)
        self.sub1 = self.create_subscription(RouteState, "/planning/mission_planning/route_selector/main/state", self.on_msg1, qos)
        self.sub2 = self.create_subscription(RouteState, "/planning/mission_planning/route_selector/mrm/state", self.on_msg2, qos)
        self.sub2 = self.create_subscription(RouteState, "/planning/mission_planning/state", self.on_msg3, qos)
        self.msg1 = None
        self.msg2 = None
        self.msg3 = None
        self.timer = self.create_timer(1.0, self.on_timer)

    def on_msg1(self, msg):
        self.msg1 = msg

    def on_msg2(self, msg):
        self.msg2 = msg

    def on_msg3(self, msg):
        self.msg3 = msg

    def on_timer(self):
        self.print("MAIN", self.msg1)
        self.print("MRM ", self.msg2)
        self.print("plan", self.msg3)
        self.get_logger().info("=" * 50)

    def print(self, label, msg):
        self.get_logger().info(f"{label}: {self.to_str(msg):<12} curr: {self.to_hex(msg)}")

    @staticmethod
    def to_str(state):
        if state is None:
            return "NONE"
        if state.state == RouteState.UNKNOWN:
            return "UNKNOWN"
        if state.state == RouteState.INITIALIZING:
            return "INITIALIZING"
        if state.state == RouteState.UNSET:
            return "UNSET"
        if state.state == RouteState.PLANNING:
            return "PLANNING"
        if state.state == RouteState.SET:
            return "SET"
        if state.state == RouteState.REROUTING:
            return "REROUTING"
        if state.state == RouteState.ARRIVED:
            return "ARRIVED"
        if state.state == RouteState.ABORTED:
            return "ABORTED"
        return "-----"


    @staticmethod
    def to_hex(state):
        if state is None:
            return "----"
        return "".join(f"{i:02x}" for i in state.uuid.uuid)

if __name__ == '__main__':
    try:
        rclpy.init()
        rclpy.spin(RouteStateViewer())
        rclpy.shutdown()
    except KeyboardInterrupt:
        pass
