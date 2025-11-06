<script setup>
import { computed, onBeforeMount, ref, watch } from "vue";
import axios, { all } from "axios";
import _ from "lodash";
import { storeToRefs } from "pinia";
import useUserStore from "@/stores/userStore";
import Cookies from "js-cookie";

const content = ref([]);
const content_type = ref([]);
const users = ref([]);
const contentPictureRefAdd = ref();
const contentPictureRefEdit = ref();
const modalPictureRef = ref("");
const contentAddImageURL = ref();
const contentEditImageURL = ref();

const selectedUser = ref(null);
const filteredContent = ref([]);

function filterContentByUser() {
  if (selectedUser.value === null) {
    filteredContent.value = content.value;
  } else if (selectedUser.value.user_id == userId.value && isSuperUser.value) {
    filteredContent.value = content.value;
  } else {
    filteredContent.value = content.value.filter(
      (contentItem) => contentItem.user === selectedUser.value.id
    );
  }
}

watch(selectedUser, filterContentByUser);

const statistics = ref({});
async function fetchStatistics() {
  try {
    const r = await axios.get("/api/content/stats/");
    statistics.value = r.data;
  } catch (error) {
    console.error("Ошибка при получении статистики:", error);
  }
}

const userStore = useUserStore();
const { isSuperUser, isAuthenticated, username, userId } =
  storeToRefs(userStore);

const contentToAdd = ref({});
const contentToEdit = ref({});

const contentTypeByID = computed(() => {
  return _.keyBy(content_type.value, (x) => x.id);
});
///////////////////////////////////////////////////////////////////////
async function onContentAdd() {
  const formData = new FormData();

  formData.append("picture", contentPictureRefAdd.value.files[0]);

  formData.set("episode_name", contentToAdd.value.episode_name);
  formData.set("type", contentToAdd.value.type);
  formData.set("episode", contentToAdd.value.episode);
  formData.set("volume", contentToAdd.value.volume);
  formData.set("description", contentToAdd.value.description);

  await axios.post("/api/content/", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  await fetchContent();
}

async function contentAddPictureChange() {
  contentAddImageURL.value = URL.createObjectURL(
    contentPictureRefAdd.value.files[0]
  );
}

async function contentEditPictureChange() {
  contentEditImageURL.value = URL.createObjectURL(
    contentPictureRefEdit.value.files[0]
  );
}

async function onRemoveClick(content) {
  await axios.delete(`/api/content/${content.id}/`);
  fetchContent();
}

async function onContentEditClick(content) {
  contentToEdit.value = { ...content };
}

async function onImageClick(picture) {
  modalPictureRef.value = picture;
}

async function onUpdateContent() {
  const formData = new FormData();

  formData.append("picture", contentPictureRefEdit.value.files[0]);

  formData.set("episode_name", contentToEdit.value.episode_name);
  formData.set("type", contentToEdit.value.type);
  formData.set("episode", contentToEdit.value.episode);
  formData.set("volume", contentToEdit.value.volume);
  formData.set("description", contentToEdit.value.description);

  await axios.patch(`/api/content/${contentToEdit.value.id}/`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  await fetchContent();
}

///////////////////////////////////////////////////////////////////////
async function fetchContentTypes() {
  const r = await axios.get("/api/content-types/");
  content_type.value = r.data;
}

async function fetchContent() {
  const r = await axios.get("/api/content/");
  content.value = r.data;
}

async function fetchUsers() {
  if (isSuperUser.value) {
    const r = await axios.get("/api/users/");
    users.value = r.data;
  }
  return null;
}

let isFetching = false;

async function fetchAllData() {
  axios.defaults.headers.common["X-CSRFToken"] = Cookies.get("csrftoken");
  if (!isFetching) {
    isFetching = true;
    await fetchStatistics();
    await fetchContentTypes();
    await fetchContent();
    await fetchUsers();
    await filterContentByUser();
    isFetching = false;
  }
}

onBeforeMount(fetchAllData);
</script>

<template>
  <div class="container-fluid">
    <div class="p-2">
      <div class="col">
        <form @submit.prevent.stop="onContentAdd">
          <div class="row custom-row background-filler m-1">
            <div class="my-1 col-12 col-md">
              <div class="form-floating add-subitem">
                <input
                  type="text"
                  class="form-control custom-color"
                  v-model="contentToAdd.episode_name"
                  required
                />
                <label for="floatingInput">Название эпизода</label>
              </div>
            </div>

            <div class="my-1 col-12 col-md">
              <div class="form-floating add-subitem">
                <input
                  type="text"
                  class="form-control custom-color"
                  v-model="contentToAdd.description"
                  required
                />
                <label for="floatingInput">Описание эпизода</label>
              </div>
            </div>

            <div class="my-1 col-12 col-md">
              <div class="form-floating add-subitem">
                <select
                  class="form-select custom-color"
                  v-model="contentToAdd.type"
                  required
                >
                  <option
                    :value="t.id"
                    v-for="t in content_type"
                    v-bind:key="t.id"
                  >
                    {{ t.name }}
                  </option>
                </select>
                <label for="floatingInput">Тип</label>
              </div>
            </div>

            <div class="my-1 col-12 col-md">
              <div class="form-floating add-subitem">
                <input
                  type="number"
                  class="form-control custom-color"
                  v-model="contentToAdd.episode"
                  required
                />
                <label for="floatingInput">№ эпизода</label>
              </div>
            </div>

            <div class="my-1 col-12 col-md">
              <div class="form-floating add-subitem">
                <input
                  type="number"
                  class="form-control custom-color"
                  v-model="contentToAdd.volume"
                  required
                />
                <label for="floatingInput">№ раздела</label>
              </div>
            </div>

            <div class="my-1 col-12 col-md-1" style="align-content: center">
              <input
                class="form-control"
                type="file"
                ref="contentPictureRefAdd"
                @change="contentAddPictureChange"
                required
              />
            </div>

            <div class="my-1 col-12 col-md-auto">
              <div
                style="
                  display: flex;
                  justify-content: center;
                  align-items: center;
                  height: 100%;
                "
              >
                <button class="btn btn-outline-success btn-lg">
                  <i class="bi bi-database-fill-add"></i>
                </button>
              </div>
            </div>
          </div>

          <div v-if="isSuperUser" class="row custom-row background-filler m-1">
            <div class="my-1 col-12 col-md">
              <div class="form-floating add-subitem">
                <select
                  class="form-select custom-color"
                  v-model="selectedUser"
                  @change="filterContentByUser"
                >
                  <option :value="t" v-for="t in users" v-bind:key="t.id">
                    {{ t.username }}
                  </option>
                </select>
                <label for="floatingInput">Фильтр по пользователю</label>
              </div>
            </div>
          </div>

          <div class="row custom-row background-filler m-1">
            <div class="my-1 col-12 col-md">
              <div class="row">
                <div class="col-12">
                  <h5 class="text-center" style="margin-bottom: 20px">
                    <strong>Статистика всего контента</strong>
                  </h5>
                </div>
                <div class="col-12 col-md-6">
                  <div class="statistic-item">
                    <strong>Всего:&nbsp;</strong> {{ statistics.count }}
                  </div>
                </div>
                <div class="col-12 col-md-6">
                  <div class="statistic-item">
                    <strong>Среднее количество:&nbsp;</strong>
                    {{ statistics.avg }}
                  </div>
                </div>
                <div class="col-12 col-md-6">
                  <div class="statistic-item">
                    <strong>Максимум:&nbsp;</strong> {{ statistics.max }}
                  </div>
                </div>
                <div class="col-12 col-md-6">
                  <div class="statistic-item">
                    <strong>Минимум:&nbsp;</strong> {{ statistics.min }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </form>
      </div>

      <div class="col m-1">
        <div
          v-for="item in content"
          :key="item.id"
          class="row-auto content-item background-filler"
        >
          <div>{{ item.episode_name }}</div>
          <div class="content-subitem">
            {{ contentTypeByID[item.type]?.name }}
          </div>
          <div class="content-subitem">{{ item.episode }} эпизод</div>
          <div class="content-subitem">{{ item.volume }} раздел</div>
          <div>
            <img
              :src="item.picture"
              style="max-height: 58px; cursor: zoom-in"
              @click="onImageClick(item.picture)"
              data-bs-toggle="modal"
              data-bs-target="#imageContentModal"
            />
          </div>
          <button
            class="btn btn-outline-info"
            @click="onContentEditClick(item)"
            data-bs-toggle="modal"
            data-bs-target="#descriptionContentModal"
          >
            <i class="bi bi-three-dots"></i>
          </button>
          <button
            class="btn btn-outline-primary"
            @click="onContentEditClick(item)"
            data-bs-toggle="modal"
            data-bs-target="#editContentModal"
          >
            <i class="bi bi-pencil-fill"></i>
          </button>
          <button class="btn btn-outline-danger" @click="onRemoveClick(item)">
            <i class="bi bi-trash-fill"></i>
          </button>
        </div>
      </div>

      <div class="modal fade" id="editContentModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="exampleModalLabel">
                Редактировать эпизод
              </h1>
            </div>
            <div class="modal-body">
              <div class="col">
                <div class="row">
                  <div class="col">
                    <div class="col-auto">
                      <form
                        class="form-floating"
                        @submit.prevent.stop="onUpdateContent"
                      >
                        <input
                          type="text"
                          class="form-control"
                          id="floatingInputValue"
                          v-model="contentToEdit.episode_name"
                          required
                        />
                        <label for="floatingInputValue">Название</label>
                      </form>
                    </div>
                  </div>
                  <div class="col">
                    <div class="col-auto">
                      <div class="form-floating">
                        <select class="form-select" id="floatingSelect">
                          <option
                            selected
                            :value="t.id"
                            v-for="t in content_type"
                            v-bind:key="t.id"
                          >
                            {{ t.name }}
                          </option>
                        </select>
                        <label for="floatingSelect">Тип</label>
                      </div>
                    </div>
                  </div>
                  <div class="col">
                    <div class="col-auto">
                      <form
                        class="form-floating"
                        @submit.prevent.stop="onUpdateContent"
                      >
                        <input
                          type="number"
                          class="form-control"
                          id="floatingInputValue"
                          v-model="contentToEdit.episode"
                          required
                        />
                        <label for="floatingInputValue">№ эпизода</label>
                      </form>
                    </div>
                  </div>
                  <div class="col">
                    <div class="col-auto">
                      <form
                        class="form-floating"
                        @submit.prevent.stop="onUpdateContent"
                      >
                        <input
                          type="number"
                          class="form-control"
                          id="floatingInputValue"
                          v-model="contentToEdit.volume"
                          required
                        />
                        <label for="floatingInputValue">№ раздела</label>
                      </form>
                    </div>
                  </div>
                </div>

                <div class="row my-2">
                  <div class="my-1" style="align-content: center">
                    <input
                      class="form-control"
                      type="file"
                      ref="contentPictureRefEdit"
                      @change="contentEditPictureChange"
                      required
                    />
                  </div>
                </div>

                <div class="row my-2">
                  <div class="col">
                    <div class="form-floating">
                      <textarea
                        class="form-control"
                        placeholder="Leave a comment here"
                        id="floatingTextarea"
                        v-model="contentToEdit.description"
                        style="height: 350px"
                      ></textarea>
                      <label for="floatingInputValue">Описание эпизода</label>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-outline-danger"
                data-bs-dismiss="modal"
              >
                <i class="bi bi-x-square-fill"></i>
              </button>
              <button
                data-bs-dismiss="modal"
                type="button"
                class="btn btn-outline-success"
                @click="onUpdateContent"
              >
                <i class="bi bi-floppy2-fill"></i>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="modal fade" id="descriptionContentModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="exampleModalLabel">
                Описание эпизода
              </h1>
            </div>
            <div class="modal-body">
              <div class="row">
                <div class="form-floating">
                  <textarea
                    class="form-control"
                    placeholder="Leave a comment here"
                    id="floatingTextarea"
                    v-model="contentToEdit.description"
                    style="height: 350px"
                    readonly
                  ></textarea>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-outline-danger"
                data-bs-dismiss="modal"
              >
                <i class="bi bi-x-square-fill"></i>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="modal fade" id="imageContentModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="exampleModalLabel">
                Изображение
              </h1>
            </div>
            <div class="modal-body">
              <img
                :src="modalPictureRef"
                class="img-fluid"
                alt="Увеличенное изображение"
              />
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-outline-danger"
                data-bs-dismiss="modal"
              >
                <i class="bi bi-x-square-fill"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.content-item {
  padding: 0.5rem;
  margin: 0.5rem 0;
  border-radius: 6px;
  border: solid 2px #7790b8;
  display: grid;
  grid-template-columns: 1fr auto auto auto auto auto auto auto;
  gap: 16px;
  align-items: center;
  align-content: center;
}

.statistic-item {
  padding: 10px;
  background-color: #fefef9;
  border-radius: 5px;
  margin-bottom: 10px; 
  display: flex;
  justify-content: center;
}

.content-subitem {
  background-color: #fefef9;
  border-radius: 6px;
  border: solid 2px #7790b8;
  padding: 12.5px;
}

.add-subitem {
  border: solid 2px #7790b8;
  border-radius: 6px;
}

.custom-color {
  background-color: #fefef9;
}

.background-filler {
  background-color: #e7eef9;
  border-radius: 6px;
  border: solid 2px #7790b8;
  padding: 5px;
}

@media (max-width: 1500px) {
  .custom-row > div {
    flex: 0 0 auto;
    max-width: auto;
  }
}

.content-item {
  padding: 0.5rem;
  margin: 0.5rem 0;
  border-radius: 6px;
  display: grid;
  grid-template-columns: 1fr auto auto auto auto auto auto auto;
  gap: 16px;
  align-items: center;
  align-content: center;
}

@media (max-width: 1000px) {
  .content-item {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .content-item > div,
  .content-item img,
  .content-item button {
    width: 100%;
    text-align: center;
    margin: 5px 0;
  }

  .content-item img {
    max-height: auto;
    margin-top: 10px;
  }
}
</style>