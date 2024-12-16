<script setup>
import { computed, onBeforeMount, ref } from "vue";
import axios from "axios";
import _ from "lodash";

const content = ref([]);
const content_type = ref([]);
const contentPictureRef = ref();
const contentAddImageURL = ref();

const contentToAdd = ref({});
const contentToEdit = ref({});

const contentTypeByID = computed(() => {
  return _.keyBy(content_type.value, (x) => x.id);
});

const showZoomImageContainer = ref(false);
const zoomImageUrl = ref("");

function showZoomImage(imageUrl) {
  zoomImageUrl.value = imageUrl;
  showZoomImageContainer.value = true;
}

function hideZoomImage() {
  showZoomImageContainer.value = false;
}
///////////////////////////////////////////////////////////////////////
async function onContentAdd() {
  const formData = new FormData();

  formData.append("picture", contentPictureRef.value.files[0]);

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
    contentPictureRef.value.files[0]
  );
}

async function onRemoveClick(content) {
  await axios.delete(`/api/content/${content.id}/`);
  fetchContent();
}

async function onContentEditClick(content) {
  contentToEdit.value = { ...content };
}

async function onUpdateContent() {
  await axios.patch(`/api/content/${contentToEdit.value.id}/`, {
    ...contentToEdit.value,
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

onBeforeMount(async () => {
  await fetchContent();
  await fetchContentTypes();
});
</script>

<template>
  <div class="container-fluid">
    <div class="p-2">
      <form @submit.prevent.stop="onContentAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                v-model="contentToAdd.episode_name"
                required
              />
              <label for="floatingInput">Название эпизода</label>
            </div>
          </div>

          <div class="col-auto">
            <input
              class="form-control"
              type="file"
              ref="contentPictureRef"
              @change="contentAddPictureChange"
              required
            />
          </div>

          <div class="col-auto">
            <img :src="contentAddImageURL" style="max-height: 60px" required />
          </div>

          <div class="col-auto">
            <div class="form-floating">
              <select class="form-select" v-model="contentToAdd.type" required>
                <option
                  :value="t.id"
                  v-for="t in content_type"
                  v-bind:key="t.id"
                >
                  {{ t.name }}
                </option>
              </select>
              <label for="floatingInput">Тип контента</label>
            </div>
          </div>

          <div class="col-auto">
            <div class="form-floating">
              <input
                type="number"
                class="form-control"
                v-model="contentToAdd.episode"
                required
              />
              <label for="floatingInput">Номер эпизода</label>
            </div>
          </div>

          <div class="col-auto">
            <div class="form-floating">
              <input
                type="number"
                class="form-control"
                v-model="contentToAdd.volume"
                required
              />
              <label for="floatingInput">Номер раздела</label>
            </div>
          </div>

          <div class="col-auto" style="align-content: center">
            <button class="btn btn-outline-success btn-lg">
              <i class="bi bi-database-fill-add"></i>
            </button>
          </div>
        </div>
      </form>

      <div v-if="loading">Гружу...</div>

      <div>
        <div v-for="item in content" class="content-item" v-bind:key="item">
          <div>{{ item.episode_name }}</div>
          <div>{{ contentTypeByID[item.id]?.name }}</div>
          <div>{{ item.episode }}</div>
          <div>{{ item.volume }}</div>
          <!-- <div v-show="item.picture">
            <img :src="item.picture" style="max-height: 60px" />
          </div> -->
          <img
            :src="item.picture"
            style="max-height: 60px; cursor: pointer"
            @click="showZoomImage(item.picture)"
          />
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
                        <label for="floatingInputValue">Название эпизода</label>
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
                        <label for="floatingSelect">Тип контента</label>
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
    </div>

    <div
      class="zoom-image-container"
      :class="{ active: showZoomImageContainer }"
      @click="hideZoomImage"
    >
      <img :src="zoomImageUrl" alt="Увеличенное изображение" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.content-item {
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 6px;
  display: grid;
  grid-template-columns: 1fr auto auto auto auto auto auto auto;
  gap: 16px;
  align-items: center;
  align-content: center;
}

.custom-modal-width {
  max-width: 1000px;
  width: 900px;
  max-height: 90vh;
  overflow-y: auto;
}

.zoom-image-container {
  position: fixed;
  left: 0;
  top: 40px;
  right: 0;
  bottom: 0;
  display: block;
  padding: 1rem;
  backdrop-filter: blur(4px);
  z-index: 100;
  transform: scale(0.2, 0.2);
  transition: all 0.2s ease-out;
  opacity: 0;
  height: 0;
  overflow: hidden;
}

.zoom-image-container.active {
  opacity: 1;
  transform: scale(1, 1);
  height: auto;
}

.zoom-image-container img {
  height: 100%;
  width: 100%;
  object-fit: contain;
}
</style>
