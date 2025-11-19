#include <iostream>
#include <chrono>
#include <thread>

class RosbotClass {
public:
    RosbotClass() : x(0.0), t(now()) {}
    void move() {
        // simulate movement for 1 second
        std::this_thread::sleep_for(std::chrono::milliseconds(500));
        x += 1.0; // moved 1 meter
        t = now();
    }
    float get_position(int idx) {
        // idx 1->x, 2->y, 3->z (mock)
        if (idx == 1) return x;
        return 0.0;
    }
    double get_time() {
        return t;
    }
private:
    float x;
    double t;
    double now() {
        using namespace std::chrono;
        return duration_cast<duration<double>>(steady_clock::now().time_since_epoch()).count();
    }
};

#include <ros/ros.h> // will be ignored if ROS not present, but include kept for parity

int main(int argc, char **argv) {
    // ros::init(argc, argv, "rosbot_node"); // skip actual ROS init in mock
    RosbotClass rosbot;
    rosbot.move();
    float x1 = rosbot.get_position(1);
    double t1 = rosbot.get_time();
    std::cout << "x1 = " << x1 << " t1 = " << t1 << std::endl;

    rosbot.move();
    float x2 = rosbot.get_position(1);
    double t2 = rosbot.get_time();
    std::cout << "x2 = " << x2 << " t2 = " << t2 << std::endl;

    double speed = (x2 - x1)/(t2 - t1);
    std::cout << "Mean speed (m/s): " << speed << std::endl;
    std::cout << "Speed <= 1.0? " << (speed <= 1.0) << std::endl;
    return 0;
}
