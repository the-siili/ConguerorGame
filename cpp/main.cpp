#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <unordered_map>
#include <vector>
#include <queue>
#include <limits>
#include <optional>
#include <algorithm>
#include <string>

namespace py = pybind11;


struct Vec2{
    float x;
    float y;
    bool operator==(const Vec2& other) const {
        return x == other.x && y == other.y;
    }
    std::string repr() const {
        return "Vec2(" + std::to_string(x) + ", " + std::to_string(y) + ")";
    }
    bool operator==(const Vec2& b)
    {
        return (x == b.x && y == b.y);
    }
    bool operator<(const Vec2& a, const Vec2& b)
    {
        return (x < b.x && y < b.y);
    }
};


// Hash support if used as unordered_map key
namespace std {
    template <>
    struct hash<Vec2> {
        size_t operator()(const Vec2& v) const {
            return std::hash<float>()(v.x) ^ (std::hash<float>()(v.y) << 1);
        }
    };
}

using Graph = std::unordered_map<Vec2, std::vector<std::pair<Vec2, float>>>;


std::optional<std::vector<Vec2>> shortest_path(const Graph& graph, const Vec2& start, const Vec2& end) {
    using PQItem = std::pair<float, Vec2>;
    std::priority_queue<PQItem, std::vector<PQItem>, std::greater<>> queue;

    std::unordered_map<Vec2, float> distances;
    std::unordered_map<Vec2, std::optional<Vec2>> previous;

    for (const auto& [Vec2, _] : graph) {
        distances[Vec2] = std::numeric_limits<float>::infinity();
        previous[Vec2] = std::nullopt;
    }
    distances[start] = 0.0f;

    queue.emplace(0.0f, start);

    while (!queue.empty()) {
        auto [current_distance, current_Vec2] = queue.top();
        queue.pop();

        if (current_Vec2 == end) {
            break;
        }

        if (current_distance > distances[current_Vec2]) {
            continue;
        }

        for (const auto& [neighbor, weight] : graph.at(current_Vec2)) {
            float distance = current_distance + weight;
            if (distance < distances[neighbor]) {
                distances[neighbor] = distance;
                previous[neighbor] = current_Vec2;
                queue.emplace(distance, neighbor);
            }
        }
    }

    // Reconstruct path
    if (distances[end] == std::numeric_limits<float>::infinity()) {
        return std::nullopt; // No path
    }

    std::vector<Vec2> path;
    Vec2 current = end;

    while (previous[current].has_value()) {
        path.push_back(current);
        current = previous[current].value();
    }
    path.push_back(start);

    return path;
}

PYBIND11_MODULE(dijkstra, handle){
    handle.doc() = "this is doc";
    handle.def("shortest_path", &shortest_path);

    py::class_<Vec2>(handle, "Vec2")
        .def(py::init<int, int>())
        .def_readwrite("x", &Vec2::x)
        .def_readwrite("y", &Vec2::y)
        .def("__repr__", &Vec2::repr)
        .def("__eq__", &Vec2::operator==)
        .def("__hash__", [](const Vec2& v) {
            return std::hash<Vec2>()(v);
        });
}