// The browser pulls from the local Python menu source when the AI server is running.
const fallbackMenuItems = [
    { name: "Spicy Burger", price: 8.75, category: "Entrees", popularityRating: 4.8 },
    { name: "Large Soda", price: 2.5, category: "Drinks", popularityRating: 4.1 },
    { name: "Chocolate Cookie", price: 1.95, category: "Desserts", popularityRating: 4.6 },
    { name: "Iced Tea", price: 2.75, category: "Drinks", popularityRating: 4.4 },
    { name: "Loaded Fries", price: 4.95, category: "Entrees", popularityRating: 4.5 },
    { name: "Vanilla Shake", price: 3.95, category: "Desserts", popularityRating: 4.7 },
    { name: "Chicken Wrap", price: 7.25, category: "Entrees", popularityRating: 4.3 },
    { name: "Strawberry Lemonade", price: 3.1, category: "Drinks", popularityRating: 4.2 },
    { name: "Apple Pie Bites", price: 3.5, category: "Desserts", popularityRating: 4.5 },
    { name: "Buffalo Tenders", price: 6.85, category: "Entrees", popularityRating: 4.6 }
];

let menuItems = [...fallbackMenuItems];

// The order array acts like the Order.selected_items list in models.py.
const currentOrder = [];
const orderHistory = [];
let completedOrders = 0;
let currentView = [...menuItems];
let activeCategory = "All";
let searchTerm = "";
let popularityDescending = true;
let priceAscending = true;

const menuList = document.getElementById("menu-list");
const orderList = document.getElementById("order-list");
const historyList = document.getElementById("history-list");
const recommendationList = document.getElementById("recommendation-list");
const itemCount = document.getElementById("item-count");
const averagePrice = document.getElementById("average-price");
const orderTotal = document.getElementById("order-total");
const verifiedStatus = document.getElementById("verified-status");
const visibleCount = document.getElementById("visible-count");
const activeCategoryLabel = document.getElementById("active-category");
const completedOrdersCount = document.getElementById("completed-orders-count");
const topRecommendation = document.getElementById("top-recommendation");
const categoryFilter = document.getElementById("category-filter");
const searchInput = document.getElementById("search-input");
const sortButton = document.getElementById("sort-button");
const priceSortButton = document.getElementById("price-sort-button");
const resetButton = document.getElementById("reset-button");
const clearOrderButton = document.getElementById("clear-order-button");
const completeOrderButton = document.getElementById("complete-order-button");
const emptyResults = document.getElementById("empty-results");
const aiPrompt = document.getElementById("ai-prompt");
const aiSubmitButton = document.getElementById("ai-submit-button");
const aiResponseText = document.getElementById("ai-response-text");

async function loadMenuFromServer() {
    try {
        const response = await fetch("/api/menu");
        if (!response.ok) {
            throw new Error(`Menu request failed with status ${response.status}`);
        }

        const payload = await response.json();
        if (Array.isArray(payload.items) && payload.items.length > 0) {
            menuItems = payload.items;
        }
    } catch (_error) {
        // The static fallback keeps the demo usable even when only index.html is opened directly.
        menuItems = [...fallbackMenuItems];
    }

    currentView = [...menuItems];
}

function getRecommendedItems() {
    // Recommendations stay logical by following the category of the most recent choice.
    if (currentOrder.length === 0) {
        return [...menuItems]
            .sort((left, right) => right.popularityRating - left.popularityRating)
            .slice(0, 3);
    }

    const lastItem = currentOrder[currentOrder.length - 1];

    return menuItems
        .filter((item) => item.category === lastItem.category && item.name !== lastItem.name)
        .sort((left, right) => right.popularityRating - left.popularityRating)
        .slice(0, 3);
}

function renderRecommendations() {
    const recommendations = getRecommendedItems();
    recommendationList.innerHTML = "";

    if (recommendations.length === 0) {
        const emptyState = document.createElement("li");
        emptyState.textContent = "Add another item to generate a recommendation.";
        recommendationList.appendChild(emptyState);
        topRecommendation.textContent = "None";
        return;
    }

    recommendations.forEach((item) => {
        const listItem = document.createElement("li");
        listItem.textContent = `${item.name} (${item.category}) - rating ${item.popularityRating}`;
        recommendationList.appendChild(listItem);
    });

    topRecommendation.textContent = recommendations[0].name;
}

function renderMenu(items) {
    menuList.innerHTML = "";
    visibleCount.textContent = String(items.length);
    activeCategoryLabel.textContent = activeCategory;
    emptyResults.hidden = items.length !== 0;

    items.forEach((item) => {
        const card = document.createElement("article");
        card.className = "menu-card";

        card.innerHTML = `
            <span class="tag">${item.category}</span>
            <h3>${item.name}</h3>
            <p class="meta">Price: $${item.price.toFixed(2)}</p>
            <p class="meta">Popularity: ${item.popularityRating}</p>
            <button type="button">Add to Order</button>
        `;

        // Each card button pushes one item into the active order summary.
        card.querySelector("button").addEventListener("click", () => {
            currentOrder.push(item);
            renderOrder();
            renderRecommendations();
        });

        menuList.appendChild(card);
    });
}

function renderOrder() {
    orderList.innerHTML = "";

    if (currentOrder.length === 0) {
        const emptyMessage = document.createElement("li");
        emptyMessage.textContent = "No items added yet.";
        orderList.appendChild(emptyMessage);
    } else {
        currentOrder.forEach((item, index) => {
            const listItem = document.createElement("li");
            listItem.className = "order-row";

            const text = document.createElement("span");
            text.textContent = `${item.name} - $${item.price.toFixed(2)}`;

            const removeButton = document.createElement("button");
            removeButton.type = "button";
            removeButton.className = "secondary-button";
            removeButton.textContent = "Remove";
            removeButton.addEventListener("click", () => {
                currentOrder.splice(index, 1);
                renderOrder();
                renderRecommendations();
            });

            listItem.appendChild(text);
            listItem.appendChild(removeButton);
            orderList.appendChild(listItem);
        });
    }

    // The total matches the Order.calculate_total logic from the Python model.
    const total = currentOrder.reduce((sum, item) => sum + item.price, 0);
    const average = currentOrder.length === 0 ? 0 : total / currentOrder.length;
    itemCount.textContent = String(currentOrder.length);
    averagePrice.textContent = average.toFixed(2);
    orderTotal.textContent = total.toFixed(2);
    verifiedStatus.textContent = completedOrders > 0 ? "Yes" : "No";
    completedOrdersCount.textContent = String(completedOrders);
}

function renderHistory() {
    historyList.innerHTML = "";

    if (orderHistory.length === 0) {
        const emptyState = document.createElement("li");
        emptyState.textContent = "No completed orders yet.";
        historyList.appendChild(emptyState);
        return;
    }

    orderHistory.forEach((order, index) => {
        const listItem = document.createElement("li");
        listItem.textContent = `Order ${index + 1}: ${order.items.join(", ")} | Total: $${order.total.toFixed(2)}`;
        historyList.appendChild(listItem);
    });
}

function applyFilters() {
    currentView = menuItems.filter((item) => {
        const matchesCategory = activeCategory === "All" || item.category === activeCategory;
        const matchesSearch = item.name.toLowerCase().includes(searchTerm.toLowerCase());
        return matchesCategory && matchesSearch;
    });

    renderMenu(currentView);
}

function sortByPopularity() {
    currentView = [...currentView].sort(
        (left, right) => popularityDescending
            ? right.popularityRating - left.popularityRating
            : left.popularityRating - right.popularityRating
    );
    popularityDescending = !popularityDescending;
    renderMenu(currentView);
}

function sortByPrice() {
    currentView = [...currentView].sort(
        (left, right) => priceAscending
            ? left.price - right.price
            : right.price - left.price
    );
    priceAscending = !priceAscending;
    renderMenu(currentView);
}

categoryFilter.addEventListener("change", (event) => {
    activeCategory = event.target.value;
    applyFilters();
});

searchInput.addEventListener("input", (event) => {
    searchTerm = event.target.value;
    applyFilters();
});

sortButton.addEventListener("click", () => {
    sortByPopularity();
});

priceSortButton.addEventListener("click", () => {
    sortByPrice();
});

resetButton.addEventListener("click", () => {
    categoryFilter.value = "All";
    searchInput.value = "";
    activeCategory = "All";
    searchTerm = "";
    popularityDescending = true;
    priceAscending = true;
    applyFilters();
});

clearOrderButton.addEventListener("click", () => {
    currentOrder.length = 0;
    renderOrder();
    renderRecommendations();
});

completeOrderButton.addEventListener("click", () => {
    if (currentOrder.length === 0) {
        window.alert("Add at least one item before completing the order.");
        return;
    }

    const total = currentOrder.reduce((sum, item) => sum + item.price, 0);
    orderHistory.push({
        items: currentOrder.map((item) => item.name),
        total
    });

    completedOrders += 1;
    currentOrder.length = 0;
    renderOrder();
    renderHistory();
    renderRecommendations();
    window.alert("Order completed. Customer is now verified.");
});

aiSubmitButton.addEventListener("click", async () => {
    const message = aiPrompt.value.trim();
    if (!message) {
        aiResponseText.textContent = "Type a request first so the assistant has something to answer.";
        return;
    }

    aiResponseText.textContent = "Thinking...";

    try {
        const response = await fetch("/api/assistant", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message,
                orderItems: currentOrder.map((item) => item.name)
            })
        });

        const payload = await response.json();
        aiResponseText.textContent = payload.reply || "The assistant did not return a response.";
    } catch (_error) {
        aiResponseText.textContent =
            "The AI endpoint is not available. Start the local ai_server.py process to use Gemini.";
    }
});

async function initializeApp() {
    await loadMenuFromServer();
    applyFilters();
    renderOrder();
    renderHistory();
    renderRecommendations();
}

initializeApp();
